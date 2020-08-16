#ifndef ALLOC_HH
#define ALLOC_HH

#include <cstdlib>

void *aligned_alloc(size_t alignment, size_t size)
{
    if (alignment < sizeof(void *) && sizeof(void *) % alignment == 0) {
        alignment = sizeof(void *);
    }
    void *ptr = nullptr;
    posix_memalign(&ptr, alignment, size);
    return ptr;
}

#endif
