import numpy as np
from pathlib import Path


def load_data(folder):
    files = Path(folder).iterdir()

    data = []

    for file in files:
        if file.is_file():
            trajectory = np.loadtxt(file)
            data.append((file.name, trajectory))

    return data


def range_query(data, latitude=None, longitude=None, time=None):
    results = []

    for filename, trajectory in data:
        for point in trajectory:

            if latitude is not None:
                if not (latitude[0] <= point[0] <= latitude[1]):
                    continue

            if longitude is not None:
                if not (longitude[0] <= point[1] <= longitude[1]):
                    continue

            if time is not None:
                if not (time[0] <= point[2] <= time[1]):
                    continue

            # Point matches all specified conditions
            results.append((filename, trajectory))
            break

    return results


def compare_results(original_results, simplified_results):

    original_traj_names = []
    simplified_traj_names = []

    for filename, trajectory in original_results:
        original_traj_names.append(filename)

    for filename, trajectory in simplified_results:
        simplified_traj_names.append(filename)

    matching = []

    for filename in original_traj_names:
        if filename in simplified_traj_names:
            matching.append(filename)

    if len(simplified_traj_names) > 0:
        precision = len(matching) / len(simplified_traj_names)
    else:
        precision = 0

    if len(original_traj_names) > 0:
        recall = len(matching) / len(original_traj_names)
    else:
        recall = 0

    if precision + recall > 0:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0

    return f1, precision, recall, matching

# Load all trajectories
data = load_data("Geolife_out")

print("Number of trajectories:", len(data))


# Range query
results = range_query(
    data,
    latitude=(39.98, 39.99),
    longitude=(116.5, 116.6)
)


# Print matching filenames
print("Matching trajectories:", len(results))

for filename, trajectory in results:
    print("Filenames:", filename)

# Run identical queries
og_results = range_query(
    data,
    latitude=(39.98, 39.99),
    longitude=(116.5, 116.6)
 )

simp_results = range_query(
    data,
    latitude=(39.98, 39.99),
    longitude=(116.5, 116.6)
)


# Compare results
f1, precision, recall, matching = compare_results(og_results,simp_results)


# Print comparison
print("\n--- Query Comparison ---")
print("Original results:", len(og_results))
print("Simplified results:", len(simp_results))
print("Matching trajectories:", len(matching))
print("F1 score:", f1)

print("Precision:", precision)
print("Recall:", recall)

