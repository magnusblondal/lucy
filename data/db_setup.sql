-- DROP TABLE IF EXISTS bots CASCADE;
-- CREATE TABLE bots (
--   id                  TEXT              NOT NULL,
--   name                TEXT              NOT NULL,
--   description         TEXT              NULL,
--   active              boolean           DEFAULT false,
--   max_positions       INT               NOT NULL,
--   capital             NUMERIC           NOT NULL,
--   entry_size          NUMERIC           NOT NULL,
--   so_size             NUMERIC           NOT NULL,
--   max_safety_orders   INT               NOT NULL,
--   allow_shorts        boolean           DEFAULT false,
--   created_at          timestamp         DEFAULT CURRENT_TIMESTAMP,
--   PRIMARY KEY (id)
-- );


-- DROP TABLE IF EXISTS positions CASCADE;
-- CREATE TABLE positions (
--   id                  TEXT              NOT NULL,
--   bot_id              TEXT              NOT NULL,
--   symbol              TEXT              NOT NULL,
--   side                TEXT              NOT NULL,
--   profit              NUMERIC           NOT NULL,
--   profit_pct          NUMERIC           NOT NULL,
--   created_at          timestamp         DEFAULT CURRENT_TIMESTAMP,
--   CONSTRAINT fk_positions_bot FOREIGN KEY (bot_id) REFERENCES  bots (id),
--   PRIMARY KEY (id)
-- );

-- DROP TABLE IF EXISTS signals CASCADE;
-- CREATE TABLE signals (
--   id                  TEXT              NOT NULL,
--   position_id         TEXT              NOT NULL,
--   bot_id              TEXT              NOT NULL,
--   strategy            TEXT              NOT NULL,
--   ticker              TEXT              NOT NULL,
--   side                TEXT              NOT NULL,
--   signal_type         TEXT              NOT NULL,
--   interval            TEXT              NOT NULL,
--   bar_open_time       timestamp         NOT NULL,
--   signal_time         timestamp         NOT NULL,
--   close               NUMERIC           NOT NULL,
--   created_at          timestamp         DEFAULT CURRENT_TIMESTAMP,
--   -- CONSTRAINT fk_signals_positions FOREIGN KEY (position_id) REFERENCES  positions (id),
--   CONSTRAINT fk_signals_bot   FOREIGN KEY (bot_id) REFERENCES  bots (id),
--   PRIMARY KEY (id)
-- );

-- DROP TABLE IF EXISTS orders CASCADE;
-- CREATE TABLE orders (
--   id                    TEXT              NOT NULL,
--   position_id           TEXT              NOT NULL,
--   bot_id                TEXT              NOT NULL,
--   symbol                TEXT              NOT NULL,
--   qty                   NUMERIC           NOT NULL,
--   price                 NUMERIC           NOT NULL,
--   order_type            TEXT              NOT NULL,
--   side                  TEXT              NOT NULL,
--   type                  TEXT              NOT NULL,
--   filled                NUMERIC           NOT NULL,
--   limit_price           NUMERIC           NOT NULL,
--   reduce_only           boolean           NOT NULL,
--   order_created_at      timestamp         NOT NULL,  
--   last_update_timestamp timestamp         NOT NULL,
--   exchange_id           TEXT              NULL,
--   created_at            timestamp         DEFAULT CURRENT_TIMESTAMP,
--   -- CONSTRAINT fk_orders_positions FOREIGN KEY (position_id) REFERENCES positions (id),
--   CONSTRAINT fk_orders_bot   FOREIGN KEY (bot_id) REFERENCES  bots (id),
--   PRIMARY KEY (id)
-- );

DROP TABLE IF EXISTS fills CASCADE;
CREATE TABLE fills (
  id                  TEXT              NOT NULL,
  instrument          TEXT              NOT NULL,
  time                timestamp         NOT NULL,
  price               NUMERIC           NOT NULL,
  buy                 boolean           NOT NULL,
  qty                 NUMERIC           NOT NULL,
  remaining_order_qty NUMERIC           NOT NULL,
  order_id            TEXT              NOT NULL,
  fill_type           TEXT              NOT NULL, 
  fee_paid            NUMERIC           NOT NULL,
  fee_currency        TEXT              NOT NULL,
  taker_order_type    TEXT              NOT NULL,
  order_type          TEXT              NOT NULL,
  cli_ord_id          TEXT              NOT NULL,
  created_at          timestamp         DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);