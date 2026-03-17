CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS call_records (
    id SERIAL PRIMARY KEY,
    customer_phone TEXT NOT NULL,
    channel TEXT NOT NULL,
    transcript TEXT,
    ai_response TEXT,
    outcome TEXT CHECK (outcome IN ('resolved', 'escalated', 'failed')),
    confidence_score FLOAT CHECK (confidence_score BETWEEN 0 AND 1),
    csat_score INT CHECK (csat_score BETWEEN 1 AND 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration INT
);

-- Index for fast lookup by phone (used in get_recent)
CREATE INDEX idx_phone ON call_records(customer_phone);

-- Index for time-based queries (recent calls)
CREATE INDEX idx_created_at ON call_records(created_at);

-- Index for outcome analysis
CREATE INDEX idx_outcome ON call_records(outcome);
"""


import asyncpg

class CallRecordRepository:

    def __init__(self, db_url):
        self.db_url = db_url

    async def connect(self):
        self.conn = await asyncpg.connect(self.db_url)

    async def close(self):
        await self.conn.close()

    # Save record
    async def save(self, call_data: dict):
        query = """
        INSERT INTO call_records (
            customer_phone, channel, transcript, ai_response,
            outcome, confidence_score, csat_score, duration
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
        """

        await self.conn.execute(
            query,
            call_data["customer_phone"],
            call_data["channel"],
            call_data["transcript"],
            call_data["ai_response"],
            call_data["outcome"],
            call_data["confidence_score"],
            call_data.get("csat_score"),
            call_data.get("duration")
        )

    # Get recent calls
    async def get_recent(self, phone: str, limit: int = 5):
        query = """
        SELECT * FROM call_records
        WHERE customer_phone = $1
        ORDER BY created_at DESC
        LIMIT $2
        """

        rows = await self.conn.fetch(query, phone, limit)
        return [dict(row) for row in rows]
    
    async def get_low_resolution_intents(conn):
        query = """
    SELECT transcript AS intent,
           COUNT(*) FILTER (WHERE outcome = 'resolved') * 1.0 / COUNT(*) AS resolution_rate,
    AVG(csat_score) AS avg_csat
    FROM call_records
    WHERE created_at >= NOW() - INTERVAL '7 days'
    GROUP BY transcript
    ORDER BY resolution_rate ASC
    LIMIT 5;
    """

        rows = await conn.fetch(query)
        return [dict(row) for row in rows]