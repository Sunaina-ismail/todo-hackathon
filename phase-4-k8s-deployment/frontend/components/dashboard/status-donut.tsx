'use client'

import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'

interface StatusDonutProps {
  data: Array<{ name: string; value: number; color: string }>
  height?: number
}

export function StatusDonut({ data, height = 250 }: StatusDonutProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={90}
          dataKey="value"
          stroke="#090E0C"
          strokeWidth={2}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color || '#BEF264'} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: '#111814',
            border: '1px solid #BEF264',
            borderRadius: '8px',
            color: '#FFFFFF'
          }}
        />
      </PieChart>
    </ResponsiveContainer>
  )
}
