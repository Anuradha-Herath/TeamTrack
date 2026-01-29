/**
 * Card container with optional title and padding.
 */
export function Card({ title, children, className = '' }) {
  return (
    <div className={`rounded-xl border border-gray-200 bg-white shadow-sm ${className}`}>
      {title && (
        <div className="border-b border-gray-200 px-4 py-3">
          <h3 className="text-sm font-semibold text-gray-900">{title}</h3>
        </div>
      )}
      <div className={title ? 'p-4' : 'p-4'}>{children}</div>
    </div>
  )
}
