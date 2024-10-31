import numpy as np
import re
from collections import defaultdict

class QuantumLanguageModel:
    def __init__(self, initial_text):
        # Clean and initialize with initial text
        self.words = self.clean_text(initial_text)
        self.unique_words = list(set(self.words))
        self.matrix_size = len(self.unique_words)
        
        # Initialize matrices
        self.binary_matrix = np.zeros((self.matrix_size, self.matrix_size), dtype=int)
        self.entanglement_matrix = np.zeros((self.matrix_size, self.matrix_size), dtype=complex)
        self.anti_entanglement_matrix = np.zeros((self.matrix_size, self.matrix_size), dtype=int)
        
        # Initialize wave functions for each unique word
        self.wave_functions = {word: np.random.random() + 1j * np.random.random() for word in self.unique_words}
        
        # Populate initial matrices
        self.update_binary_matrix(self.words)
        self.update_entanglement_matrix()
    
    def clean_text(self, text):
        # Remove punctuation and lowercase the text
        return re.sub(r'[^\w\s]', '', text.lower()).split()
    
    def update_binary_matrix(self, words):
        # Populate the binary matrix based on co-occurrence in words
        co_occurrence = defaultdict(lambda: defaultdict(int))
        for i, word in enumerate(words):
            for j in range(i + 1, len(words)):
                if words[j] != word:
                    co_occurrence[word][words[j]] += 1
                    co_occurrence[words[j]][word] += 1

        # Update the binary matrix based on co-occurrence
        for i, word1 in enumerate(self.unique_words):
            for j, word2 in enumerate(self.unique_words):
                if co_occurrence[word1][word2] > 0:
                    self.binary_matrix[i, j] = 1

    def update_entanglement_matrix(self):
        # Calculate entanglement matrix based on wave functions
        for i, word1 in enumerate(self.unique_words):
            for j, word2 in enumerate(self.unique_words):
                self.entanglement_matrix[i, j] = self.wave_functions[word1] * np.conj(self.wave_functions[word2])

    def update_anti_entanglement_matrix(self, new_text):
        # Handle new text input and update anti-entanglement matrix dynamically
        words = self.clean_text(new_text)
        encountered = set(words)
        
        # Expand vocabulary and matrices for new words
        for word in encountered:
            if word not in self.unique_words:
                self.unique_words.append(word)
                self.matrix_size = len(self.unique_words)
                self.entanglement_matrix.resize((self.matrix_size, self.matrix_size))
                self.anti_entanglement_matrix.resize((self.matrix_size, self.matrix_size))
                self.binary_matrix.resize((self.matrix_size, self.matrix_size))
                self.wave_functions[word] = np.random.random() + 1j * np.random.random()
        
        # Update anti-entanglement values
        for i, word1 in enumerate(self.unique_words):
            if word1 not in encountered:
                for word2 in encountered:
                    idx1, idx2 = self.unique_words.index(word1), self.unique_words.index(word2)
                    self.anti_entanglement_matrix[idx1, idx2] += 1
                    self.anti_entanglement_matrix[idx2, idx1] += 1

    def collapse_matrix(self, query_word):
        # Collapse entanglement matrix based on a query word
        query_idx = self.unique_words.index(query_word)
        collapsed_state = np.abs(self.entanglement_matrix[query_idx, :])
        ranked_words = sorted(zip(self.unique_words, collapsed_state), key=lambda x: -x[1])
        return ranked_words
    
    def principal_components(self):
        # Calculate eigenvalues and eigenvectors of the entanglement matrix
        eigenvalues, eigenvectors = np.linalg.eig(self.entanglement_matrix)
        principal_components = sorted(zip(eigenvalues, self.unique_words), key=lambda x: -np.abs(x[0]))
        return principal_components

    def phrase_wave_function(self, phrase):
        # Create a composite wave function for a phrase
        phrase_words = self.clean_text(phrase)
        composite_wave = sum(self.wave_functions[word] for word in phrase_words if word in self.wave_functions)
        return composite_wave

    def coherence_score(self, phrase1, phrase2):
        # Calculate coherence score between two phrases
        phrase1_wave = self.phrase_wave_function(phrase1)
        phrase2_wave = self.phrase_wave_function(phrase2)
        coherence = np.dot(np.conj(phrase1_wave), phrase2_wave)
        return coherence

# Example Usage
initial_text = "quantum machine learning involves complex quantum states and probabilities. quantum computers process data using quantum bits."
model = QuantumLanguageModel(initial_text)

# Updating model with new text
model.update_anti_entanglement_matrix("quantum fields evolve differently from classical fields.")

# Collapse for query word 'quantum'
collapsed_state_quantum = model.collapse_matrix("quantum")

# Get principal components (eigenwords)
principal_eigenwords = model.principal_components()

# Calculate coherence score between two phrases
phrase_coherence = model.coherence_score("quantum entanglement creates new possibilities", "complex states involve quantum coherence")

# Display the results
{
    "Collapsed State (Quantum)": collapsed_state_quantum,
    "Principal Components (Eigenwords)": principal_eigenwords,
    "Phrase Coherence Score": phrase_coherence
}

"""
{'Collapsed State (Quantum)': [('using', 1.0793515493295875),
  ('complex', 0.9278216233086194),
  ('learning', 0.8913305895937257),
  ('fields', 0.8421381700994542),
  ('process', 0.7622704096393138),
  ('computers', 0.715823618662683),
  ('from', 0.6808561074116176),
  ('evolve', 0.6777767211081287),
  ('machine', 0.6464891342359593),
  ('involves', 0.6211629167253594),
  ('bits', 0.6134968787628631),
  ('classical', 0.5852708686160755),
  ('probabilities', 0.562252285665988),
  ('states', 0.5232179495947449),
  ('quantum', 0.5005987732211391),
  ('data', 0.4183875713170509),
  ('differently', 0.3157782395569614),
  ('and', 0.2592778594733412)],
 'Principal Components (Eigenwords)': [((4.9791831533882+0.0269922194773643j),
   'complex'),
  ((1.0746074146367284+0.4085115995032292j), 'using'),
  ((-0.23567791362046767+1.0432337826171076j), 'quantum'),
  ((-0.8490270368464945-0.4389553189295058j), 'process'),
  ((-0.4918879275113536+0.5145212156255171j), 'probabilities'),
  ((0.38349737778137016-0.4703101523575058j), 'learning'),
  ((0.04029681782638304-0.5949404148211367j), 'bits'),
  ((-0.433856722497078+0.21395804195408227j), 'involves'),
  ((0.18228962142119584+0.1742383426630238j), 'and'),
  ((0.14869412718434105-0.028945272916044925j), 'states'),
  (0j, 'data'),
  (0j, 'computers'),
  (0j, 'machine'),
  (0j, 'classical'),
  (0j, 'from'),
  (0j, 'differently'),
  (0j, 'fields'),
  (0j, 'evolve')],
 'Phrase Coherence Score': (3.6742597063814104+0.5506886333035974j)}
"""
