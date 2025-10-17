// netlify/functions/trades.js
exports.handler = async (event, context) => {
  // Handle CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
  }

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' }
  }

  try {
    const { method, path } = event
    const { trades } = require('../api.js')

    switch (method) {
      case 'GET':
        if (path.includes('/stats')) {
          const stats = await trades.getStats()
          return {
            statusCode: 200,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify(stats)
          }
        } else {
          const { data, error } = await trades.getAll()
          return {
            statusCode: 200,
            headers: { ...headers, 'Content-Type': 'application/json' },
            body: JSON.stringify({ data, error })
          }
        }

      case 'POST':
        const tradeData = JSON.parse(event.body)
        const { data, error } = await trades.create(tradeData)
        return {
          statusCode: 201,
          headers: { ...headers, 'Content-Type': 'application/json' },
          body: JSON.stringify({ data, error })
        }

      default:
        return {
          statusCode: 405,
          headers,
          body: JSON.stringify({ error: 'Method not allowed' })
        }
    }
  } catch (error) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    }
  }
}
