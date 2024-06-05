import sys
import math
import numpy as np
import matplotlib.pyplot as plt


def parse_pdb_file(file_path):
    waters = []
    atoms = []
    unique_waters = {}
    with open(file_path, "r") as pdb_file:
        for line in pdb_file:
            if line.startswith("HETATM") and "HOH" in line[17:20]:
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                residue_seq = int(line[22:26].strip())
                if residue_seq not in unique_waters:
                    unique_waters[residue_seq] = {
                        "x": x,
                        "y": y,
                        "z": z,
                        "residue_seq": residue_seq,
                    }
            elif (
                line.startswith("ATOM")
                or (line.startswith("HETATM") and "HOH" not in line[17:20])
            ) and line[76:78].strip() != "H":
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                atoms.append({"x": x, "y": y, "z": z})
    waters = list(unique_waters.values())
    return np.array(waters), np.array(atoms)


def calculate_distance(atom1, atom2):
    return math.sqrt(
        (atom1["x"] - atom2["x"]) ** 2
        + (atom1["y"] - atom2["y"]) ** 2
        + (atom1["z"] - atom2["z"]) ** 2
    )


def find_closest_distances(waters, atoms):
    distances = []
    for water in waters:
        min_distance = float("inf")
        for atom in atoms:
            distance = calculate_distance(water, atom)
            if distance < min_distance:
                min_distance = distance
        distances.append(min_distance)
    return distances


def plot_distances(waters, distances):
    residue_seq_numbers = [water["residue_seq"] for water in waters]
    arbitrary_order = list(range(1, len(waters) + 1))
    avg_distance = np.mean(distances)
    min_distance = np.min(distances)
    max_distance = np.max(distances)

    plt.figure(figsize=(14, 7))
    plt.scatter(arbitrary_order, distances, color="b", label="Distances")
    plt.axhline(
        avg_distance, color="g", linestyle="--",
        label=f"Average: {avg_distance:.2f} Å"
    )
    plt.axhline(
        min_distance, color="r", linestyle="--",
        label=f"Min: {min_distance:.2f} Å"
    )
    plt.axhline(
        max_distance, color="y", linestyle="--",
        label=f"Max: {max_distance:.2f} Å"
    )

    for i, txt in enumerate(residue_seq_numbers):
        plt.annotate(txt, (arbitrary_order[i], distances[i]), fontsize=8,
                     ha="center")

    plt.xlabel("Water Molecule")
    plt.ylabel("Closest Distance to Non-Water Atom (Å)")
    plt.title("Closest Distance from Water Molecules to Non-Water Atoms")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python find_water_distances.py <pdb_file_path>")
        sys.exit(1)

    pdb_file_path = sys.argv[1]

    print("Parsing PDB file...")
    waters, atoms = parse_pdb_file(pdb_file_path)
    print(
        f"Found {len(waters)} unique water molecules and {len(atoms)}" +
        " non-water atoms (excluding hydrogens)."
    )

    print("Calculating closest distances...")
    distances = find_closest_distances(waters, atoms)

    print("Plotting distances...")
    plot_distances(waters, distances)
