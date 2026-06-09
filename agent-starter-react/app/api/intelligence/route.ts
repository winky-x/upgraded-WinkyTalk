import { NextRequest, NextResponse } from 'next/server';

interface TelemetryData {
  id: string;
  lat: number;
  lon: number;
  velocity: number;
  category: 'plane' | 'ship';
}

interface Alert {
  id: string;
  timestamp: string;
  level: 'CRITICAL' | 'WARNING';
  message: string;
  lat: number;
  lon: number;
}

export async function POST(req: NextRequest) {
  try {
    const data: TelemetryData[] = await req.json();

    if (!Array.isArray(data)) {
      return NextResponse.json(
        [{ id: crypto.randomUUID(), timestamp: new Date().toISOString(), level: 'WARNING', message: 'Invalid telemetry payload structure', lat: 0, lon: 0 }],
        { status: 400 }
      );
    }

    const alerts: Alert[] = [];

    for (const item of data) {
      if (item.category === 'ship') {
        if (item.velocity < 2) {
          alerts.push({
            id: crypto.randomUUID(),
            timestamp: new Date().toISOString(),
            level: 'CRITICAL',
            message: `Chokepoint Detected: Ship ${item.id} moving at ${item.velocity.toFixed(2)} knots.`,
            lat: item.lat,
            lon: item.lon
          });
        }
      } else if (item.category === 'plane') {
        // Erratic velocity: commercial flights usually cruise at 400-500 knots. Let's say > 600 or < 100 is erratic.
        if (item.velocity > 600) {
          alerts.push({
            id: crypto.randomUUID(),
            timestamp: new Date().toISOString(),
            level: 'WARNING',
            message: `Vector Anomaly: Flight ${item.id} exhibiting supersonic velocity (${item.velocity.toFixed(2)} knots).`,
            lat: item.lat,
            lon: item.lon
          });
        } else if (item.velocity < 100 && item.velocity > 0) {
           alerts.push({
            id: crypto.randomUUID(),
            timestamp: new Date().toISOString(),
            level: 'WARNING',
            message: `Vector Anomaly: Flight ${item.id} exhibiting abnormally low velocity (${item.velocity.toFixed(2)} knots).`,
            lat: item.lat,
            lon: item.lon
          });
        }
      }
    }

    // Sort alerts by priority: CRITICAL first, then WARNING
    alerts.sort((a, b) => {
      if (a.level === 'CRITICAL' && b.level !== 'CRITICAL') return -1;
      if (a.level !== 'CRITICAL' && b.level === 'CRITICAL') return 1;
      return 0;
    });

    // Top 3 highest priority alerts
    const topAlerts = alerts.slice(0, 3);

    return NextResponse.json(topAlerts);
  } catch (error) {
    console.error("Intelligence Engine Error:", error);
    // Flawless error handling, never 500
    return NextResponse.json([
      {
         id: crypto.randomUUID(),
         timestamp: new Date().toISOString(),
         level: 'WARNING',
         message: 'Intelligence Engine encountered an internal evaluation fault. Fail-safe triggered.',
         lat: 0,
         lon: 0
      }
    ]);
  }
}
