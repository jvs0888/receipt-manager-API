CREATE TABLE user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_username UNIQUE (username)
);

CREATE TABLE receipt (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    products JSON,
    payment JSON,
    total FLOAT,
    rest FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
);

CREATE INDEX idx_user_id ON user(id);
CREATE INDEX idx_user_username ON user(username);
CREATE INDEX idx_receipt_user_id ON receipt(user_id);
CREATE INDEX idx_receipt_id ON receipt(id);
