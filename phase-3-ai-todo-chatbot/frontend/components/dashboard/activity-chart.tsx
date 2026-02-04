'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

interface ActivityChartProps {
  data: Array<{
    date: string
    created: number
    completed: number
    updated: number
    label: string
  }>
  height?: number
}

export function ActivityChart({ data, height = 300 }: ActivityChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
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
        />
        <Legend
          wrapperStyle={{ color: '#FFFFFF' }}
        />
        <Line
          type="monotone"
          dataKey="created"
          stroke="#BEF264"
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
          animationDuration={800}
        />
        <Line
          type="monotone"
          dataKey="completed"
          stroke="#10B981"
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
          animationDuration={800}
        />
        <Line
          type="monotone"
          dataKey="updated"
          stroke="#F59E0B"
          strokeWidth={2}
          strokeDasharray="5 5"
          dot={{ r: 4 }}
          animationDuration={800}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
