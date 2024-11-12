import itertools
import math

class JoinTree:
    def cost(self, directory):
        raise NotImplementedError()

    def cardinality(self, directory):
        raise NotImplementedError()

    def get_relations(self):
        raise NotImplementedError()

    def contains(self, relation):
        raise NotImplementedError()

    def has_cross_product(self, directory):
        raise NotImplementedError()


class Join(JoinTree):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def cost(self, directory):
        return self.cardinality(directory) + self.left.cost(directory) + self.right.cost(directory)

    def cardinality(self, directory):
        factor = self.get_selectivity_product(directory)
        return math.ceil(factor * self.left.cardinality(directory) * self.right.cardinality(directory))

    def get_relations(self):
        relations = self.left.get_relations() + self.right.get_relations()
        return relations

    def contains(self, relation):
        return self.left.contains(relation) or self.right.contains(relation)

    def has_cross_product(self, directory):
        if self.is_cross_product(directory):
            return True
        return self.left.has_cross_product(directory) or self.right.has_cross_product(directory)

    def is_cross_product(self, directory):
        return self.get_selectivity_product(directory) == 1

    def get_selectivity_product(self, directory):
        factor = 1
        left_relations = self.left.get_relations()
        right_relations = self.right.get_relations()
        for l in left_relations:
            for r in right_relations:
                factor *= directory.get_selectivity(l, r)
        return factor

    def __str__(self):
        return f"({self.left} ⋈ {self.right})"


class Relation(JoinTree):
    def __init__(self, relation):
        self.relation = relation

    def cost(self, directory):
        return 0

    def cardinality(self, directory):
        return directory.get_size(self.relation)

    def get_relations(self):
        return [self.relation]

    def contains(self, relation):
        return self.relation == relation

    def has_cross_product(self, directory):
        return False

    def __str__(self):
        return self.relation



class DummyFileDirectory:
    def __init__(self, filepath):
        self.relations = {}
        self.selectivities = {}
        with open(filepath, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 2:
                    self.relations[parts[0]] = int(parts[1])
                elif len(parts) == 3:
                    self.selectivities[(parts[0], parts[1])] = float(parts[2])
                    self.selectivities[(parts[1], parts[0])] = float(parts[2])

    def get_size(self, relation):
        return self.relations.get(relation, 0)

    def get_selectivity(self, relation_a, relation_b):
        return self.selectivities.get((relation_a, relation_b), 1)

    def get_relations(self):
        return list(self.relations.items())


def compute_greedy1(directory):
    relations = [Relation(r[0]) for r in directory.get_relations()]
    while len(relations) > 1:
        min_cost = float('inf')
        best_pair = None
        for i in range(len(relations)):
            for j in range(i + 1, len(relations)):
                join = Join(relations[i], relations[j])
                cost = join.cost(directory)
                if cost < min_cost:
                    min_cost = cost
                    best_pair = (i, j)
        i, j = best_pair
        new_join = Join(relations[i], relations[j])
        del relations[j], relations[i]
        relations.append(new_join)
    return relations[0]


def compute_best_plan(directory):
    relations = [Relation(r[0]) for r in directory.get_relations()]
    best_plan = None
    min_cost = float('inf')

    for perm in itertools.permutations(relations):
        plan = perm[0]
        for rel in perm[1:]:
            plan = Join(plan, rel)
        cost = plan.cost(directory)
        if cost < min_cost:
            min_cost = cost
            best_plan = plan
    return best_plan


def compute_worst_plan(directory):
    relations = [Relation(r[0]) for r in directory.get_relations()]
    worst_plan = None
    max_cost = -1

    for perm in itertools.permutations(relations):
        plan = perm[0]
        for rel in perm[1:]:
            plan = Join(plan, rel)
        cost = plan.cost(directory)
        if cost > max_cost:
            max_cost = cost
            worst_plan = plan
    return worst_plan


if __name__ == "__main__":
    
    from os import path
    current_dir = path.dirname(__file__)
    file_path = path.join(current_dir, 'data.txt')
    
    # file_path = "data.txt"
    directory = DummyFileDirectory(file_path)

    print("Greedy1 Plan:")
    greedy1_plan = compute_greedy1(directory)
    print(f"{greedy1_plan} with cost {greedy1_plan.cost(directory)}")

    print("\nBest Plan:")
    best_plan = compute_best_plan(directory)
    print(f"{best_plan} with cost {best_plan.cost(directory)}")

    print("\nWorst Plan:")
    worst_plan = compute_worst_plan(directory)
    print(f"{worst_plan} with cost {worst_plan.cost(directory)}")
