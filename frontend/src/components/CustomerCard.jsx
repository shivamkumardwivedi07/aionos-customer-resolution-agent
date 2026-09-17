import React from 'react';
import { User, Award, Plane, Clock, AlertCircle, History, CheckCircle2 } from 'lucide-react';

export default function CustomerCard({ customers, selectedCustomer, onSelectCustomer }) {
  if (!selectedCustomer) return null;

  const { customer, booking } = selectedCustomer;

  const getTierBadge = (tier) => {
    switch (tier.toLowerCase()) {
      case 'gold':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      case 'platinum':
        return 'bg-purple-500/20 text-purple-300 border-purple-500/40';
      case 'silver':
        return 'bg-slate-300/20 text-slate-200 border-slate-400/40';
      default:
        return 'bg-sky-500/20 text-sky-300 border-sky-500/40';
    }
  };

  const getStatusBadge = (status) => {
    switch (status?.toLowerCase()) {
      case 'cancelled':
        return 'bg-rose-500/20 text-rose-300 border-rose-500/40';
      case 'delayed':
        return 'bg-amber-500/20 text-amber-300 border-amber-500/40';
      default:
        return 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
    }
  };

  return (
    <div className="bg-slate-900/60 rounded-xl border border-slate-800 p-4 shadow-md space-y-4">
      {/* Customer Selector Tabs */}
      <div>
        <label className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 mb-2 block">
          Select Customer (Demo Mode)
        </label>
        <div className="grid grid-cols-3 gap-1.5 p-1 bg-slate-950/80 rounded-lg border border-slate-800">
          {customers.map((c) => {
            const isSelected = c.customer.customer_id === customer.customer_id;
            return (
              <button
                key={c.customer.customer_id}
                onClick={() => onSelectCustomer(c)}
                className={`py-1.5 px-2 text-xs font-medium rounded-md transition-all truncate text-center ${
                  isSelected
                    ? 'bg-sky-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                {c.customer.name.split(' ')[0]}
              </button>
            );
          })}
        </div>
      </div>

      {/* Customer Profile Header */}
      <div className="pt-2 border-t border-slate-800/80">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-sm font-bold text-white flex items-center gap-1.5">
              <User className="w-4 h-4 text-sky-400" />
              {customer.name}
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">{customer.contact.email}</p>
          </div>
          <span className={`px-2 py-0.5 text-[11px] font-semibold rounded-full border ${getTierBadge(customer.loyalty_tier)}`}>
            {customer.loyalty_tier}
          </span>
        </div>
      </div>

      {/* Disrupted Booking Card */}
      {booking && (
        <div className="bg-slate-950/70 rounded-lg border border-slate-800/90 p-3 space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-semibold text-sky-400 flex items-center gap-1">
              <Plane className="w-3.5 h-3.5" />
              {booking.flight_number}
            </span>
            <span className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded border ${getStatusBadge(booking.status)}`}>
              {booking.status} {booking.delay_hours > 0 ? `(${booking.delay_hours}h)` : ''}
            </span>
          </div>

          <div className="text-xs space-y-1">
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">Route:</span>
              <span className="font-medium">{booking.route}</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">PNR:</span>
              <span className="font-mono font-medium text-amber-300">{booking.booking_reference}</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">Date:</span>
              <span>{booking.date}</span>
            </div>
            <div className="flex justify-between text-slate-300">
              <span className="text-slate-400">Scheduled:</span>
              <span>{booking.scheduled_departure}</span>
            </div>
            {booking.current_departure && (
              <div className="flex justify-between text-amber-300">
                <span>Updated Departure:</span>
                <span className="font-semibold">{booking.current_departure}</span>
              </div>
            )}
            {booking.disruption_reason && (
              <div className="pt-1 text-[11px] text-slate-400 flex items-center gap-1">
                <AlertCircle className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                <span>Reason: {booking.disruption_reason}</span>
              </div>
            )}
          </div>

          {booking.return_flight && (
            <div className="pt-2 mt-2 border-t border-slate-800 text-[11px] text-slate-300">
              <div className="flex items-center justify-between text-emerald-400">
                <span className="flex items-center gap-1 font-medium">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Return: {booking.return_flight.route}
                </span>
                <span className="text-[10px] uppercase font-bold bg-emerald-500/10 px-1.5 py-0.2 rounded border border-emerald-500/20">
                  {booking.return_flight.status}
                </span>
              </div>
              <p className="text-slate-400 mt-0.5">
                {booking.return_flight.date} at {booking.return_flight.scheduled_departure}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Travel History & Complaints */}
      <div className="bg-slate-950/40 rounded-lg border border-slate-800/60 p-2.5 text-xs text-slate-400 space-y-1">
        <div className="flex items-center gap-1 font-semibold text-slate-300 text-[11px]">
          <History className="w-3.5 h-3.5 text-sky-400" />
          <span>Travel & Complaint Profile</span>
        </div>
        <p className="text-[11px]">
          • {customer.travel_history.flights_last_12_months} flights in last 12 months
        </p>
        <p className="text-[11px]">
          • Prior complaints: {customer.travel_history.prior_complaints_count}
          {customer.travel_history.previous_complaint_details && ` (${customer.travel_history.previous_complaint_details})`}
        </p>
        {customer.travel_history.previous_resolution && (
          <p className="text-[10px] text-slate-400 italic">
            Resolution: {customer.travel_history.previous_resolution}
          </p>
        )}
      </div>
    </div>
  );
}
