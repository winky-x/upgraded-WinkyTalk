import { NextResponse } from 'next/server';

interface TelemetryData {
  id: string;
  lat: number;
  lon: number;
  velocity: number;
  category: 'plane' | 'ship';
}

function generateFallbackFlights(count: number): TelemetryData[] {
  const flights: TelemetryData[] = [];
  for (let i = 0; i < count; i++) {
    flights.push({
      id: `FLIGHT-FB-${Math.random().toString(36).substring(2, 9).toUpperCase()}`,
      lat: (Math.random() * 180) - 90,
      lon: (Math.random() * 360) - 180,
      velocity: 200 + Math.random() * 400, // 200 to 600 knots
      category: 'plane'
    });
  }
  return flights;
}

function generateGhostShips(): TelemetryData[] {
  const ships: TelemetryData[] = [];
  const numShips = 4 + Math.floor(Math.random() * 2); // 4 to 5 ships
  for (let i = 0; i < numShips; i++) {
    ships.push({
      id: `GHOST-SHIP-${Math.random().toString(36).substring(2, 9).toUpperCase()}`,
      lat: -20 + Math.random() * 30, // Indian Ocean rough lat (-20 to 10)
      lon: 50 + Math.random() * 40,  // Indian Ocean rough lon (50 to 90)
      velocity: 14, // 14 knots
      category: 'ship'
    });
  }
  // Add a chokepoint ship anomaly (< 2 knots) to be flagged by intelligence engine
  ships.push({
    id: `GHOST-SHIP-ANOMALY`,
    lat: -10,
    lon: 60,
    velocity: 1.5, // < 2 knots
    category: 'ship'
  });
  return ships;
}

export async function GET() {
  try {
    let flights: TelemetryData[] = [];

    try {
      const response = await fetch('https://opensky-network.org/api/states/all', {
        next: { revalidate: 60 } // Cache for 60 seconds
      });

      if (!response.ok) {
        throw new Error(`OpenSky API responded with status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data && data.states && data.states.length >= 1000) {
        // Limit to 1500 for performance if we have too many
        const limit = Math.min(data.states.length, 1500);
        for (let i = 0; i < limit; i++) {
          const state = data.states[i];
          // state: [0: icao24, 1: callsign, 2: origin_country, 3: time_position, 4: last_contact, 5: lon, 6: lat, 7: baro_altitude, 8: on_ground, 9: velocity, ...]
          if (state[5] !== null && state[6] !== null && state[9] !== null) {
             flights.push({
               id: state[1] ? state[1].trim() : state[0],
               lat: state[6],
               lon: state[5],
               velocity: state[9] * 1.94384, // convert m/s to knots
               category: 'plane'
             });
          }
        }
      }
      
      if (flights.length < 1000) {
        flights = generateFallbackFlights(1000);
      }
    } catch (error) {
      console.warn("OpenSky API failed or rate-limited. Using fallback generator.", error);
      flights = generateFallbackFlights(1000);
    }

    // Generate ghost ships
    const ships = generateGhostShips();

    const unifiedTelemetry = [...flights, ...ships];

    return NextResponse.json(unifiedTelemetry);
  } catch (error) {
    console.error("Telemetry Endpoint Error:", error);
    // Flawless error handling, never return 500. Return fallback if everything fails.
    const fallbackFlights = generateFallbackFlights(1000);
    const fallbackShips = generateGhostShips();
    return NextResponse.json([...fallbackFlights, ...fallbackShips]);
  }
}
