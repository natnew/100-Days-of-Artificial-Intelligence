import time

class BenchmarkResult:
    def __init__(self, name: str, passed: bool, score: float, details: str = ""):
        self.name = name
        self.passed = passed
        self.score = score
        self.details = details

class BenchmarkTest:
    """
    Base class for a safety benchmarker.
    """
    def __init__(self, name: str):
        self.name = name

    def run(self, model_input) -> BenchmarkResult:
        """
        Run the test. model_input can be a Model object or text depending on test type.
        """
        raise NotImplementedError("Tests must implement run()")

class BenchmarkSuite:
    def __init__(self, name: str):
        self.name = name
        self.tests = []

    def add_test(self, test: BenchmarkTest):
        self.tests.append(test)

    def run(self, model_input) -> dict:
        results = []
        passed_count = 0
        
        start_time = time.time()
        
        for test in self.tests:
            print(f"Running test: {test.name}...")
            result = test.run(model_input)
            results.append(result)
            if result.passed:
                passed_count += 1
                
        duration = time.time() - start_time
        
        return {
            "suite_name": self.name,
            "total_tests": len(self.tests),
            "passed": passed_count,
            "failed": len(self.tests) - passed_count,
            "duration_seconds": round(duration, 2),
            "results": [
                {
                    "test": r.name, 
                    "passed": r.passed, 
                    "score": r.score,
                    "details": r.details
                } for r in results
            ]
        }
