class Matrix_algebra:
    def __init__(self, matrix=[]):

        """ Matrix algebra class for making calculations with matrice.

        Attributes:
            matrix - a series of data forming a matrix
        """
        self.matrix = matrix

    def __add__(self, other):
        
        """Function to add together two matrices
        
        Args:
            other (Matrix_algebra): Matrix_algebra instance
            
        Returns:
            matrix (Matrix_algebra): sum of two matrices
            
        """
        
        result = Matrix_algebra()
        result.matrix = [[self.matrix[i][j] + other.matrix[i][j]  for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))]
        
        return result
    
    def __sub__(self, other):
        
        """Function to subtract one matrix from another
        
        Args:
            other (Matrix_algebra): Matrix_algebra instance
            
        Returns:
            matrix (Matrix_algebra): difference between two matrices
            
        """
        
        result = Matrix_algebra()
        result.matrix = [[self.matrix[i][j] - other.matrix[i][j]  for j in range(len(self.matrix[0]))] for i in range(len(self.matrix))]
        
        return result
        
    def __mul__(self, other):
        
        """Function to multiply two matrices
        
        Args:
            other (Matrix_algebra): Matrix_algebra instance
            
        Returns:
            matrix (Matrix_algebra): difference between two matrices
            
        """
        
        result = Matrix_algebra()
        result.matrix = [[sum(a*b for a,b in zip(self_matrix_row,other_matrix_col)) for other_matrix_col in zip(*other.matrix)] for self_matrix_row in self.matrix]
        
        return result
        
