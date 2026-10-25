# Global Climate & Food Security Intelligence Platform (GCF-SIP)

## Mission & Purpose

The GCF-SIP is a production-grade strategic intelligence platform designed to support climate resilience and food security decision-making for governments, UN agencies, and development partners. The system integrates global climate and agricultural data to provide actionable insights, risk assessments, and scenario modeling capabilities.

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │ →  │  Data Ingestion  │ →  │  Validation &   │
│                 │    │   (FAOSTAT,      │    │  Quality Layer  │
│ • FAOSTAT       │    │    Climate APIs) │    │                 │
│ • Climate Data  │    │                  │    │ • Pandera       │
│ • Economic Data │    └──────────────────┘    │ • Schema Registry│
└─────────────────┘                            └─────────────────┘
                                                        │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Decision UI   │ ←  │   API Layer      │ ←  │  Analytics &    │
│                 │    │                  │    │  Modeling       │
│ • Dashboards    │    │ • FastAPI         │    │                 │
│ • Reports       │    │ • Health Checks   │    │ • Feature Store │
│ • Alerts        │    │ • Rate Limiting   │    │ • ML Models     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Development Status

### ✅ Completed Steps

**Step 1: Foundation & Repository Structure**
- Production-grade repository structure with governance artifacts
- Conda environment configuration with reproducible dependencies
- src/ layout with proper Python packaging
- Editable installation support (`pip install -e .`)
- Documentation framework and contribution guidelines

**Step 2: Data Ingestion Pipeline**
- FAOSTAT integration with resilient API handling
- Fail-safe mechanisms for upstream API downtime
- Raw data immutability and audit trail
- Standardized schema transformation
- Data quality scoring and metadata tracking

**Step 3: Platform Health & Testing**
- FastAPI health endpoint implementation
- Pytest testing framework integration
- Health check monitoring for system components
- Test coverage for ingestion pipeline
- CI/CD preparation and testing automation

### 🚧 In Progress

**Step 4: Data Contracts & Validation**
- Pandera schema enforcement
- Data contract definitions
- Validation pipeline integration
- Error handling and recovery mechanisms

### 📋 Planned Roadmap

**Step 5: Feature Engineering & Indicators**
- Climate risk indicators calculation
- Food security metrics development
- Temporal and spatial feature engineering
- Indicator normalization and standardization

**Step 6: Baseline ML Models**
- Food insecurity prediction models
- Climate impact assessment models
- Model validation and performance monitoring
- Explainability and interpretability features

**Step 7: Scenario Simulation & Uncertainty**
- Climate scenario modeling
- Funding impact simulation
- Monte Carlo uncertainty quantification
- Policy intervention analysis

**Step 8: Dashboards & Policy Views**
- Executive dashboard development
- Geographic visualization components
- Policy recommendation engine
- Alert and notification system

**Step 9: Deployment & CI/CD**
- Production deployment pipeline
- Automated testing and validation
- Infrastructure as Code implementation
- Monitoring and observability setup

## System Status

| Component | Status | Description |
|-----------|--------|-------------|
| **Data Ingestion** | 🧪 Unit-tested | Pure transformation/quality functions tested in CI; live FAOSTAT fetch has no CI mock seam yet (tracked in issues) |
| **API Layer** | 🧪 Tested | /health + router mounting asserted in CI; no public deployment |
| **Validation** | ✅ Schema-enforced | pandera schemas tested in CI (declared dependency; the test previously skipped in every environment) |
| **ML Models** | 📋 Planned | Baseline prediction models |
| **Dashboards** | 📋 Planned | Policy and executive views |
| **Deployment** | 📋 Planned | Production CI/CD pipeline |

## Environment Setup

### Prerequisites
- Python 3.9+
- Conda/Miniconda
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/collins-muchiri/Global-Climate-Food-Security-Intelligence-Platform-GCF-SIP-.git
   cd Global-Climate-Food-Security-Intelligence-Platform-GCF-SIP-
   ```

2. **Create Conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate gcf-sip
   ```

3. **Install in development mode**
   ```bash
   pip install -e .
   ```

4. **Verify installation**
   ```bash
   python -c "import src.api.main; print('Installation successful')"
   ```

## Operations & Monitoring

### Health Checks
```bash
# API health check
curl http://localhost:8000/health

# Run system tests
pytest tests/ -v
```

### Data Ingestion
```bash
# Run FAOSTAT ingestion
python -m src.ingestion.food_security_ingest

# Monitor ingestion logs
tail -f logs/ingestion.log
```

### API Operations
```bash
# Start API server
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# View API documentation
# Navigate to http://localhost:8000/docs
```

## Engineering Standards

### Quality Assurance
- **No Silent Failures**: All errors are logged and propagated
- **Deterministic Behavior**: Reproducible data processing and model outputs
- **Clear Logging**: Structured logging with appropriate severity levels
- **Data Immutability**: Raw data is never modified; all transforms are tracked

### Governance & Compliance
- **Data Ethics**: Privacy-preserving data handling and model development
- **Audit Trail**: Complete lineage tracking for all data transformations
- **Model Risk**: Systematic model validation and performance monitoring
- **Documentation**: Comprehensive technical and user documentation

### Performance & Reliability
- **Resilient Design**: Graceful handling of upstream API failures
- **Scalable Architecture**: Horizontal scaling support for data processing
- **Monitoring**: Real-time system health and performance metrics
- **Recovery**: Automated recovery mechanisms and manual override procedures

## Contributing

This is an active development project targeting UN/NGO/government-grade standards. Contributors should:

1. Follow the established branch-per-step workflow
2. Ensure all tests pass before submitting changes
3. Maintain comprehensive documentation
4. Adhere to the engineering standards outlined above
5. Review the contribution guidelines in `CONTRIBUTING.md`

## License & Usage

This project is developed for climate resilience and food security decision-making. Usage should align with the mission of supporting vulnerable communities and evidence-based policy development.

---

**Note**: This is a real system under active development. All components are designed for production deployment and operational use in climate and food security decision-making contexts.