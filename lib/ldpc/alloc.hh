#ifndef ALLOC_HH
#define ALLOC_HH

#include <cstdlib>

void *aligned_alloc(size_t alignment, size_t size)
{
    void *ptr = nullptr;
    posix_memalign(&ptr, alignment, size);
    return ptr;
}

#endif
