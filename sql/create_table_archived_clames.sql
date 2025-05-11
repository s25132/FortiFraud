CREATE TABLE archived_clames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Month TEXT,
    WeekOfMonth INTEGER,
    Make TEXT,
    AccidentArea TEXT,
    MonthClaimed TEXT,
    MaritalStatus TEXT,
    Fault TEXT,
    PolicyType TEXT,
    VehicleCategory TEXT,
    Deductible INTEGER,
    PoliceReportFiled BOOLEAN,
    AgentType TEXT,
    AddressChange_Claim TEXT,
    Year INTEGER,
    BasePolicy TEXT,
    Prediction INTEGER,
    Created DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_created ON archived_clames (Created);