'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

interface PriorityChartProps {
  data: Array<{ name: string; value: number; color: string }>
  height?: number
}

export function PriorityChart({ data, height = 300 }: PriorityChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#64748B" opacity={0.2} />
        <XAxis
          dataKey="name"
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
        />
        <Bar
          dataKey="value"
          radius={[8, 8, 0, 0]}
          animationDuration={800}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color || '#BEF264'} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
