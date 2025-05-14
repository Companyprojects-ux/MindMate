"""
Test reporting utilities.
"""
import json
import os
import datetime
from typing import Dict, Any, List, Optional
import pytest
from _pytest.runner import TestReport
from _pytest.config import Config
from _pytest.terminal import TerminalReporter

# Store test results
test_results = {
    "passed": [],
    "failed": [],
    "skipped": [],
    "errors": [],
    "xfailed": [],
    "xpassed": []
}

# Store API responses
api_responses = {}

# Store test coverage by endpoint
endpoint_coverage = {}

def register_endpoint_test(endpoint: str, method: str, test_name: str, description: str):
    """Register a test for an endpoint."""
    key = f"{method} {endpoint}"
    if key not in endpoint_coverage:
        endpoint_coverage[key] = []
    
    endpoint_coverage[key].append({
        "test_name": test_name,
        "description": description
    })

def register_api_response(test_name: str, endpoint: str, method: str, status_code: int, response_data: Any):
    """Register an API response."""
    if test_name not in api_responses:
        api_responses[test_name] = []
    
    api_responses[test_name].append({
        "endpoint": endpoint,
        "method": method,
        "status_code": status_code,
        "response_data": response_data
    })

def pytest_runtest_logreport(report: TestReport):
    """Collect test results."""
    if report.when == "call":  # Only record the final result
        result_category = report.outcome
        test_info = {
            "name": report.nodeid,
            "duration": report.duration,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        if hasattr(report, "wasxfail"):
            if report.outcome == "passed":
                result_category = "xpassed"
            else:
                result_category = "xfailed"
        
        if result_category in test_results:
            test_results[result_category].append(test_info)

def pytest_terminal_summary(terminalreporter: TerminalReporter, exitstatus: int, config: Config):
    """Generate a test report at the end of the test run."""
    # Generate report
    report_data = {
        "summary": {
            "total": len(test_results["passed"]) + len(test_results["failed"]) + len(test_results["skipped"]) + len(test_results["errors"]) + len(test_results["xfailed"]) + len(test_results["xpassed"]),
            "passed": len(test_results["passed"]),
            "failed": len(test_results["failed"]),
            "skipped": len(test_results["skipped"]),
            "errors": len(test_results["errors"]),
            "xfailed": len(test_results["xfailed"]),
            "xpassed": len(test_results["xpassed"])
        },
        "results": test_results,
        "endpoint_coverage": endpoint_coverage,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    # Save report to file
    os.makedirs("reports", exist_ok=True)
    report_file = f"reports/test_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(report_data, f, indent=2)
    
    # Print summary
    print("\nTest Report Summary:")
    print(f"Total tests: {report_data['summary']['total']}")
    print(f"Passed: {report_data['summary']['passed']}")
    print(f"Failed: {report_data['summary']['failed']}")
    print(f"Skipped: {report_data['summary']['skipped']}")
    print(f"Errors: {report_data['summary']['errors']}")
    print(f"Expected failures: {report_data['summary']['xfailed']}")
    print(f"Unexpected passes: {report_data['summary']['xpassed']}")
    print(f"Report saved to: {report_file}")

def generate_html_report():
    """Generate an HTML report from the test results."""
    # This function would generate an HTML report from the test results
    # For simplicity, we'll just use the JSON report for now
    pass

class TestReporter:
    """Test reporter for capturing test information."""
    
    def __init__(self, endpoint: str, method: str):
        self.endpoint = endpoint
        self.method = method
        self.responses = []
    
    def register_test(self, test_name: str, description: str):
        """Register a test for this endpoint."""
        register_endpoint_test(self.endpoint, self.method, test_name, description)
    
    def register_response(self, test_name: str, status_code: int, response_data: Any):
        """Register an API response."""
        register_api_response(test_name, self.endpoint, self.method, status_code, response_data)
        self.responses.append({
            "test_name": test_name,
            "status_code": status_code,
            "response_data": response_data
        })
    
    def get_responses(self):
        """Get all registered responses."""
        return self.responses
