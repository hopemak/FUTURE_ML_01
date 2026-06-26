import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';

export function LineChartCard({ title, data, dataKey, color = "#3b82f6" }) {
  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="date" tick={{fontSize: 12}} />
          <YAxis tick={{fontSize: 12}} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey={dataKey} stroke={color} strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function BarChartCard({ title, data, dataKey, color = "#10b981" }) {
  return (
    <div className="card">
      <h3 className="text-lg font-semibold mb-4 text-gray-800">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" tick={{fontSize: 12}} />
          <YAxis tick={{fontSize: 12}} />
          <Tooltip />
          <Bar dataKey={dataKey} fill={color} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
