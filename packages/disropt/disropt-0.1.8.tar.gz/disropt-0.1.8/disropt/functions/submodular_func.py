import numpy as np
import copy
from .abstract_function import AbstractFunction


class SubmodularFn(AbstractFunction):
    """Submodular AbstractFunction abstract class

    Attributes:
        V: ground set
        input_shape: cardinality of the ground set

    Args:
        input_shape: cardinality of the ground set

    Raises:
        ValueError: input_shape must be an integer positive number
    """

    def __init__(self, input_shape):

        if not isinstance(input_shape, int) or input_shape < 0:
            raise ValueError(
                "Input must be a positive integer")

        self.V = np.arange(input_shape)
        self.input_shape = (input_shape, 1)

    def eval(self, set):
        """
        Evaluate the submodular function at a given set

        Parameters:
                set (numpy.ndarray(, dtype='int')): vector

                """
        pass

    def greedy_polyhedron(self, w):
        """Greedy algorithm for finding a maximizer :math:`x` of

        .. math::
            :label: basepoly

                \\max_{x\\in B(F)}    & w^\\top x \\\\


        where :math:`B(F)` is the base polyhedron associated to the submodular function :math:`F`

        Parameters:
                w: cost direction

        Returns:
            numpy.ndarray: maximizer of :eq:`basepoly`

        Raises:
            ValueError: Input must be a numpy.ndarray with input_shape elements
                """

        w = w.flatten()
        n = len(self.V)
        Ind = np.flip(np.argsort(w))
        w = w[Ind]
        x = np.zeros((n, 1))
        empt = np.array([], dtype='int')
        Fold = self.eval(empt[:, None])
        A = np.ones((1, 1), dtype='int')
        A[0, :] = self.V[Ind[0]]
        x[Ind[0]] = self.eval(A) - Fold
        Fold = Fold + x[Ind[0]]

        for i in range(1, n):
            Anew = np.vstack((A, self.V[Ind[i]]))
            x[Ind[i]] = self.eval(Anew) - Fold
            A = Anew
            Fold = Fold + x[Ind[i]]
        return x

    def subgradient(self, x):
        """
        Evaluate a subgradient of the Lovasz extension of the
        submodular function at :math:`x`

        Parameters:
                x: vector
        Returns:
            numpy.ndarray: subgradient of the Lovasz extension of :math:`F` at :math:`x`

        Raises:
            ValueError: Input must be a numpy.ndarray with input_shape elements
                """
        return self.greedy_polyhedron(x)

    def blocksubgradient(self, x, block):
        """
        Evaluate a subgradient of the Lovasz extension of the
        submodular function at :math:`x`

        Parameters:
                x: vector
                block: vector
        Returns:
            numpy.ndarray: block subgradient of the Lovasz extension of :math:`F` at :math:`x`

        Raises:
            ValueError: Input must be a numpy.ndarray with input_shape elements
                """
        xb = copy.deepcopy(x)
        xb = xb.flatten()
        n = len(self.V)

        idx = np.where(xb[block] == np.amin(xb[block]))
        idx = np.asarray(idx)
        right_index = block[idx.item(0)]
        pivot = xb[right_index]
        rg_idx = np.arange(n)
        xb[0], xb[right_index] = xb[right_index], xb[0]
        rg_idx[0], rg_idx[right_index] = rg_idx[right_index], rg_idx[0]
        i = 1
        for j in np.arange(1, len(xb)):
            if xb[j] >= pivot:
                xb[j], xb[i] = xb[i], xb[j]
                rg_idx[j], rg_idx[i] = rg_idx[i], rg_idx[j]
                i += 1
        xb[0], xb[i - 1] = xb[i - 1], xb[0]
        rg_idx[0], rg_idx[i-1] = rg_idx[i-1], rg_idx[0]

        i_n = np.where(rg_idx == right_index)
        i_n = i_n[0].item(0)+1
        Ind = np.flip(np.argsort(xb[:i_n]))
        Ind = rg_idx[:i_n][Ind]
        lb = len(block)
        count = 1
        y = np.zeros((n, 1))

        empt = np.array([], dtype='int')
        Fold = self.eval(empt[:, None])
        A = np.ones((1, 1), dtype='int')
        A[0, :] = self.V[Ind[0]]
        prev = -1
        i = 1
        if Ind[0] in block:
            y[Ind[0]] = self.eval(A) - Fold
            Fold = Fold + y[Ind[0]]
            count += 1
            prev = 0
        while count <= lb:
            Anew = np.vstack((A, self.V[Ind[i]]))
            if Ind[i] in block:
                Fnew = self.eval(Anew)
                if i == prev+1:
                    y[Ind[i]] = Fnew - Fold
                else:
                    y[Ind[i]] = Fnew - self.eval(A)
                prev = i
                Fold = Fnew
                count += 1
            A = Anew
            i += 1
        return y


class stCutFn(SubmodularFn):
    """Submodular AbstractFunction for evaluating s-t cuts
       in a network of N+2 nodes where
       s node is the N+1 - th node and
       t node is the N+2 - th node

    Attributes:
        G: (N+2)x(N+2) communication graph
        eval_cut (numpy.ndarray,numpy.ndarray): evaluate cut value.
        eval (int): wrapper for eval_cut

    Args:
        input_shape (int): ground set cardinality
        G (numpy.ndarray): (input_shape+2)x(input_shape+2) matrix

    Raises:
        ValueError: input_shape must be an integer positive number
        ValueError: G must be a (input_shape+2)x(input_shape+2) numpy.ndarray

    """

    def __init__(self, input_shape, G):
        """Initialize the function

        """
        super(stCutFn, self).__init__(input_shape)

        if not isinstance(G, np.ndarray) or not (G.shape[0] == G.shape[1]) or not (G.shape[0] == (input_shape + 2)):
            raise ValueError(
                "Input must be a numpy.ndarray with shape {},{}".format(
                    input_shape + 2, input_shape + 2))

        self.G = G

    def eval_cut(self, G, A):
        """Evaluate cut value

        Args:
            G (numpy.ndarray): network graph
            A (numpy.ndarray): set of nodes

        Returns:
            float: cut value

        Raises:
            ValueError: A must be a numpy.ndarray with size at most (1,input_shape)

        """
        if not isinstance(
            A, np.ndarray) or (
            A.shape[1] > self.input_shape[1]) or (
                A.shape[1] > 1):
            raise ValueError(
                "Input must be a numpy.ndarray with shape at most {}".format(self.input_shape[0]))

        n = G.shape[0]
        A = np.vstack((A, n-2))  # Add s to set
        G1 = G[:, np.setdiff1d(np.arange(n), A)]
        G2 = G[:, np.setdiff1d(np.arange(n), [n - 2])]
        C = np.sum(G1[A]) - np.sum(G2[n - 2, :])
        return C

    def eval(self, A):
        """wrapper for eval cut function

        Args:
            A (numpy.ndarray): set of nodes

        Returns:
            float: cut value

        Raises:
            ValueError: A must be a numpy.ndarray with size at most (|V|, 1)
        """
        # TODO is instace np.ndarray(int)
        if not isinstance(A, np.ndarray) or (A.shape[0] > self.input_shape[0]) or (A.shape[1] > 1):
            raise ValueError(
                "Input must be a numpy.ndarray(dtype=int) with shape at most {}".format(self.input_shape[0]))
        C = self.eval_cut(self.G, A)

        return C

class Cardinality(SubmodularFn):

    def eval(self, A):
        """

        Args:
            A (numpy.ndarray): set

        Returns:
            float: cardinality of A

        Raises:
            ValueError: A must be a numpy.ndarray with size at most (|V|, 1)
        """
        # TODO is instace np.ndarray(int)
        if not isinstance(A, np.ndarray) or (A.shape[0] > self.input_shape[0]) or (A.shape[1] > 1):
            raise ValueError(
                "Input must be a numpy.ndarray(dtype=int) with shape at most {}".format(self.input_shape[0]))
        return len(A)