import sys
sys.path.insert(0, "/PeTTa/repos/omegaclaw/shared_files/7_design_artifacts/nace_adoption")
from nace_core import TruthValue, Hypothesis_TruthExpectation

tv_healthy = TruthValue(wp=9, wn=1)
print("Healthy TV: freq=" + str(round(tv_healthy.frequency, 2)) + " conf=" + str(round(tv_healthy.confidence, 2)) + " te=" + str(round(tv_healthy.truth_expectation, 2)))

tv_declining = TruthValue(wp=5, wn=5)
print("Declining TV: freq=" + str(round(tv_declining.frequency, 2)) + " conf=" + str(round(tv_declining.confidence, 2)) + " te=" + str(round(tv_declining.truth_expectation, 2)))

tv_orphan = TruthValue(wp=0, wn=10)
print("Orphan TV: freq=" + str(round(tv_orphan.frequency, 2)) + " conf=" + str(round(tv_orphan.confidence, 2)) + " te=" + str(round(tv_orphan.truth_expectation, 2)))

tv_empty = TruthValue()
print("Empty TV: freq=" + str(round(tv_empty.frequency, 2)) + " conf=" + str(round(tv_empty.confidence, 2)) + " te=" + str(round(tv_empty.truth_expectation, 2)))

print("NACE core imported and tested successfully")