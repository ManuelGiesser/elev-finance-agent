CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    booking_date DATE,
    amount NUMERIC(12,2),
    currency TEXT DEFAULT 'EUR',
    vendor TEXT,
    booking_text TEXT,
    status TEXT DEFAULT 'open',
    confidence NUMERIC(5,2),
    receipt_id INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS receipts (
    id SERIAL PRIMARY KEY,
    source TEXT,
    source_id TEXT,
    original_filename TEXT,
    current_filename TEXT,
    file_url TEXT,
    file_path TEXT,
    receipt_date DATE,
    amount NUMERIC(12,2),
    currency TEXT DEFAULT 'EUR',
    vendor TEXT,
    ocr_text TEXT,
    status TEXT DEFAULT 'new',
    duplicate_of INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS cases (
    id SERIAL PRIMARY KEY,
    transaction_id INTEGER REFERENCES transactions(id),
    category TEXT,
    status TEXT DEFAULT 'open',
    last_checked_at TIMESTAMP,
    next_step TEXT,
    due_at TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vendors (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    category TEXT,
    email TEXT,
    website TEXT,
    invoice_portal TEXT,
    search_terms TEXT,
    source_confidence TEXT DEFAULT 'unverified',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
