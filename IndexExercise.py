import random
import string
from typing import List, Set
import time

class Tuple:
    def __init__(self, id: int, string: str):
        self.id = id
        self.string = string

    def __eq__(self, other):
        return isinstance(other, Tuple) and self.id == other.id and self.string == other.string

    def __lt__(self, other):
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.string))

    def __repr__(self):
        return f"Tuple(id={self.id}, string={self.string})"


class Index:
    def __init__(self, tuples: List[Tuple]):
        self.tuples = tuples

    def get_equal_string_tuples(self, string: str) -> List[Tuple]:
        return [t for t in self.tuples if t.string == string]

    def get_greater_equals_string_tuples(self, string: str) -> List[Tuple]:
        return [t for t in self.tuples if t.string >= string]


class DenseIndex(Index):
    def __init__(self, tuples: List[Tuple]):
        super().__init__(tuples)

    def get_equal_string_tuples(self, string: str) -> List[Tuple]:
        # print(self.tuples[1:5])
        result = []
        for tuple_object in self.tuples:
            if tuple_object.string == string:
                result.append(tuple_object)
    
        return result
                    

    def get_greater_equals_string_tuples(self, string: str) -> List[Tuple]:
        result = []
        for tuple_object in self.tuples:
            if tuple_object.string >= string:
                result.append(tuple_object)
                
        return result
    
    

class DataGenerator:
    def __init__(self, num_lines: int):
        self.strings = self._generate_strings(num_lines // 10)
        self.tuples = [Tuple(i, self.get_random_string()) for i in range(num_lines)]

    def _generate_strings(self, num_strings: int) -> List[str]:
        return [self._get_alpha_numeric_string(10) for _ in range(num_strings)]

    def _get_alpha_numeric_string(self, n: int) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

    def get_random_string(self) -> str:
        return random.choice(self.strings)

    def get_sparse_attributes(self) -> Set[str]:
        sparse_set = set(self.strings)
        while len(sparse_set) < len(self.strings) // 10:
            sparse_set.add(self.get_random_string())
        return sparse_set


def dense_execution(tuples: List[Tuple], query_string: str, expected_equal_result: List[Tuple], expected_greater_result: List[Tuple]) -> bool:
    index = DenseIndex(tuples)
    return test_results(query_string, index, expected_equal_result, expected_greater_result)


def test_results(query_string: str, index: Index, expected_equal_result: List[Tuple], expected_greater_result: List[Tuple]) -> bool:
    equal_result = sorted(index.get_equal_string_tuples(query_string))
    greater_result = sorted(index.get_greater_equals_string_tuples(query_string))

    if equal_result == sorted(expected_equal_result):
        print("Equality result correct.")
    else:
        print("Equality result incorrect!")
        return False

    if greater_result == sorted(expected_greater_result):
        print("Greater result correct.")
    else:
        print("Greater result incorrect!")
        return False

    return True


if __name__ == "__main__":
    print("Index exercise")
    print("================================")
    print("Generating data...")
    gen = DataGenerator(500000)
    query_string = gen.get_random_string()
    print("================================")

    # Default execution
    print("Testing default")
    index = Index(gen.tuples)
    equal_result = sorted(index.get_equal_string_tuples(query_string))
    greater_result = sorted(index.get_greater_equals_string_tuples(query_string))
    print("================================")
    

    
    # Dense index
    print("Testing dense")
    ret = dense_execution(gen.tuples, query_string, equal_result, greater_result)
    print("================================")
    
    if not ret:
        exit(1)
    exit(0)



# def measure_performance(num_lines: int, query_string: str):
#     print(f"Creating dataset with {num_lines} tuples...")
#     gen = DataGenerator(num_lines)

#     # Measure default index execution time
#     default_index = Index(gen.tuples)
    
#     # Timing default access method
#     start_time = time.time()
#     default_equal_result = default_index.get_equal_string_tuples(query_string)
#     default_greater_result = default_index.get_greater_equals_string_tuples(query_string)
#     default_time = time.time() - start_time

#     print("Default Index Query Time:")
#     print(f"Equal Result: {default_equal_result}, Time: {default_time:.6f} seconds")
#     print(f"Greater Result: {default_greater_result}, Time: {default_time:.6f} seconds")

#     # Measure dense index execution time
#     dense_index = DenseIndex(gen.tuples)

#     # dense index access method
#     start_time = time.time()
#     dense_equal_result = dense_index.get_equal_string_tuples(query_string)
#     dense_greater_result = dense_index.get_greater_equals_string_tuples(query_string)
#     dense_time = time.time() - start_time

#     print("Dense Index Query Time:")
#     print(f"Equal Result: {dense_equal_result}, Time: {dense_time:.6f} seconds")
#     print(f"Greater Result: {dense_greater_result}, Time: {dense_time:.6f} seconds")


# if __name__ == "__main__":
#     N = 500000  # Number of tuples
#     query_string = "example"  


#     for i in range(5):  # Change this range for more executions
#         query_string = random.choice(DataGenerator(N).strings)  
#         print(f"\nExecution {i + 1} with query string: {query_string}")
#         measure_performance(N, query_string)