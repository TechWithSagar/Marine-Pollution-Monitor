# 🌊 Marine Pollution Monitoring and Alert System

### Overview

This project is a multi-agent AI system designed to autonomously monitor and detect marine pollution. It addresses the critical issue of slow and inefficient traditional monitoring methods by providing a real-time, scalable solution built on IBM Cloud. The system is comprised of three specialized AI agents that work together to turn raw data into actionable alerts, supporting the United Nations Sustainable Development Goal 14: Life Below Water.

### ✨ Features

* **Multi-Agent Architecture**: A robust system with specialized agents for data ingestion, pollution analysis, and real-time alerting.
* **Cloud-Native**: Leverages IBM Cloud services (Object Storage, Watson Studio, Watson Machine Learning) for scalability and reliability.
* **AI-Powered Detection**: Uses a `RandomForestClassifier` model to analyze environmental data and predict water potability as a proxy for pollution.
* **Actionable Alerts**: Generates immediate alerts and reports when potential pollution is detected, enabling a rapid response.
* **Interactive Dashboard**: Provides a user-friendly interface built with Streamlit for real-time monitoring and predictions.

### 🚀 Getting Started

This project requires a Python environment and an active IBM Cloud account.

#### Prerequisites

* Python 3.11 or higher
* An IBM Cloud account
* Required Python libraries (listed in `requirements.txt`)
* An IBM Cloud API key with access to your Watson Machine Learning and Cloud Object Storage instances.

#### Installation

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/](https://github.com/)[Your-Username]/[Your-Repo-Name].git
    cd [Your-Repo-Name]
    ```

2.  **Set up environment variables**:
    Create a `.env` file in the root directory and add your sensitive credentials. This file is ignored by Git to ensure security.
    ```
    WML_API_ENDPOINT="YOUR_DEPLOYMENT_API_ENDPOINT"
    WML_API_KEY="YOUR_IBM_CLOUD_API_KEY"
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### 🛠️ Usage

#### Running the Dashboard

Start the Streamlit dashboard from the terminal to interact with the deployed model:

```bash
streamlit run dashboard_app.py
