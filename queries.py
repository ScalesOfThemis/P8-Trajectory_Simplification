import numpy as np
import math
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


# Todo: Should probably separate EDR into its own function
def knn_query(data, query_trajectory, k, epsilon=0.02, time=None):
    results = []

    # Filter query trajectory by time interval
    query_points = []

    for point in query_trajectory:
        if time is not None:
            if not (time[0] <= point[2] <= time[1]):
                continue

        query_points.append(point)

    # No query points in the time interval
    if not query_points:
        return results

    # Compare query trajectory with every trajectory
    for filename, trajectory in data:

        # Filter current trajectory by same time interval
        candidate_points = []

        for point in trajectory:
            if time is not None:
                if not (time[0] <= point[2] <= time[1]):
                    continue

            candidate_points.append(point)

        # Skip trajectories with no points in the time interval
        #if not candidate_points:
            #continue

        # Create EDR table
        n = len(query_points)
        m = len(candidate_points)

        dp = [[0] * (m + 1) for _ in range(n + 1)]

        # First column
        for i in range(n + 1):
            dp[i][0] = i

        # First row
        for j in range(m + 1):
            dp[0][j] = j

        # Calculate EDR distance
        for i in range(1, n + 1):
            for j in range(1, m + 1):

                query_point = query_points[i - 1]
                candidate_point = candidate_points[j - 1]

                # Calculate Euclidean distance between the two GPS points
                distance = math.sqrt(
                                   (query_point[0] - candidate_point[0]) ** 2 +
                                   (query_point[1] - candidate_point[1]) ** 2
                           )

                # Check if the distance is smaller than epsilon
                if distance < epsilon:
                    substitution_cost = 0
                else:
                    substitution_cost = 1

                # Choose the cheapest operation from: (Deletion, insertion, or substitution)
                dp[i][j] = min(
                    dp[i - 1][j] + 1, # Deletion
                    dp[i][j - 1] + 1, # Insertion
                    dp[i - 1][j - 1] + substitution_cost # Substitution if the points match = 0 if they dont match = 1
                )

        # Bottom-right cell is the EDR distance
        edr_distance = dp[n][m]

        results.append((filename, trajectory, edr_distance))

    # Sort by EDR distance (smallest distance = most similar)
    results.sort(key=lambda result: result[2])

    # Return k most similar trajectories
    return results[:k]


# This is just for testing out the implementation
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

print("\n--- Range Query ---")

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
print("\n--- Range Query Comparison ---")
print("Original results:", len(og_results))
print("Simplified results:", len(simp_results))
print("Matching trajectories:", len(matching))
print("F1 score:", f1)

print("Precision:", precision)
print("Recall:", recall)


#Knn Query testing

query_filename, query_trajectory = data[8]

results = knn_query(
    data,
    query_trajectory,
    k=3,
    epsilon=0.02,
    time=None
)

print("Query trajectory:", query_filename)

for filename, trajectory, distance in results:
    print(filename, distance)
