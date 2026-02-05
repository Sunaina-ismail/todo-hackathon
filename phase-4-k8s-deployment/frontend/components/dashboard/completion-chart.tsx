'use client'

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import type { ChartDataPoint } from '@/lib/types'

interface CompletionChartProps {
  data: ChartDataPoint[]
  height?: number
}

export function CompletionChart({ data, height = 300 }: CompletionChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="neonLimeGradient" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#BEF264" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#BEF264" stopOpacity={0.1}/>
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#64748B" opacity={0.2} />
        <XAxis
          dataKey="label"
          stroke="#64748B"
          style={{ fontSize: '12px' }}
        />
        <YAxis
          stroke="#64748B"
          style={{ fontSize: '12px' }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: '#111814',
            border: '1px solid #BEF264',
            borderRadius: '8px',
            color: '#FFFFFF'
          }}
          labelStyle={{ color: '#FFFFFF' }}
        />
        <Area
          type="monotone"
          dataKey="value"
          stroke="#BEF264"
          strokeWidth={2}
          fillOpacity={1}
          fill="url(#neonLimeGradient)"
          animationDuration={800}
          animationEasing="ease-out"
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}
