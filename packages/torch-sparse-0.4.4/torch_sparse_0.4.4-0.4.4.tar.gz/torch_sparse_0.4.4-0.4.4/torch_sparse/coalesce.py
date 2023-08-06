import torch
import torch_scatter

from .utils.unique import unique


def coalesce(index, value, m, n, op='add'):
    """Row-wise sorts :obj:`value` and removes duplicate entries. Duplicate
    entries are removed by scattering them together. For scattering, any
    operation of `"torch_scatter"<https://github.com/rusty1s/pytorch_scatter>`_
    can be used.

    Args:
        index (:class:`LongTensor`): The index tensor of sparse matrix.
        value (:class:`Tensor`): The value tensor of sparse matrix.
        m (int): The first dimension of corresponding dense matrix.
        n (int): The second dimension of corresponding dense matrix.
        op (string, optional): The scatter operation to use. (default:
            :obj:`"add"`)

    :rtype: (:class:`LongTensor`, :class:`Tensor`)
    """

    row, col = index

    if value is None:
        _, perm = unique(row * n + col)
        index = torch.stack([row[perm], col[perm]], dim=0)
        return index, value

    uniq, inv = torch.unique(row * n + col, sorted=True, return_inverse=True)

    perm = torch.arange(inv.size(0), dtype=inv.dtype, device=inv.device)
    perm = inv.new_empty(uniq.size(0)).scatter_(0, inv, perm)
    index = torch.stack([row[perm], col[perm]], dim=0)

    op = getattr(torch_scatter, 'scatter_{}'.format(op))
    value = op(value, inv, 0, None, perm.size(0))
    value = value[0] if isinstance(value, tuple) else value

    return index, value
