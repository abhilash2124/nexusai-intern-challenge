import asyncpg

# CREATE TABLE SQL
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS call_records (
    id SERIAL PRIMARY KEY,
    customer_phone TEXT NOT NULL,
    channel TEXT NOT NULL,
    intent TEXT NOT NULL,
    transcript TEXT,
    ai_response TEXT,
    outcome TEXT CHECK (outcome IN ('resolved', 'escalated', 'failed')),
    confidence_score FLOAT CHECK (confidence_score BETWEEN 0 AND 1),
    csat_score INT CHECK (csat_score BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration INT
);

-- Index for fast lookup of customer history by phone number
CREATE INDEX IF NOT EXISTS idx_phone ON call_records(customer_phone);

-- Index for recent queries (used when fetching last 7 days data)
CREATE INDEX IF NOT EXISTS idx_created_at ON call_records(created_at);

-- Index for filtering by outcome (used in analytics queries)
CREATE INDEX IF NOT EXISTS idx_outcome ON call_records(outcome);
"""


# Repository Class
class CallRecordRepository:

    def __init__(self, db_url):
        self.db_url = db_url
        self.conn = None

    async def connect(self):
        self.conn = await asyncpg.connect(self.db_url)

    async def close(self):
        if self.conn:
            await self.conn.close()

    # Save Call Record
    async def save(self, call_data: dict):
        query = """
        INSERT INTO call_records (
            customer_phone,
            channel,
            intent,
            transcript,
            ai_response,
            outcome,
            confidence_score,
            csat_score,
            duration
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """

        await self.conn.execute(
            query,
            call_data["customer_phone"],
            call_data["channel"],
            call_data["intent"],
            call_data["transcript"],
            call_data["ai_response"],
            call_data["outcome"],
            call_data["confidence_score"],
            call_data.get("csat_score"),
            call_data.get("duration")
        )

    # Get Recent Calls
    async def get_recent(self, phone: str, limit: int = 5):
        query = """
        SELECT *
        FROM call_records
        WHERE customer_phone = $1
        ORDER BY created_at DESC
        LIMIT $2
        """

        rows = await self.conn.fetch(query, phone, limit)
        return [dict(row) for row in rows]

# Analytics Query
async def get_low_resolution_intents(conn):
    query = """
    SELECT 
        intent,
        COUNT(*) FILTER (WHERE outcome = 'resolved') * 1.0 / COUNT(*) AS resolution_rate,
        AVG(csat_score) AS avg_csat
    FROM call_records
    WHERE created_at >= NOW() - INTERVAL '7 days'
    GROUP BY intent
    ORDER BY resolution_rate ASC
    LIMIT 5;
    """

    rows = await conn.fetch(query)
    return [dict(row) for row in rows]