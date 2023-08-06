/*
 * Allocation table functions
 *
 * Copyright (C) 2008-2020, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

#if !defined( _LIBPFF_ALLOCATION_TABLE_H )
#define _LIBPFF_ALLOCATION_TABLE_H

#include <common.h>
#include <types.h>

#include "libpff_libbfio.h"
#include "libpff_libcdata.h"
#include "libpff_libcerror.h"

#if defined( __cplusplus )
extern "C" {
#endif

int libpff_allocation_table_read_data(
     libcdata_range_list_t *unallocated_block_list,
     const uint8_t *data,
     size_t data_size,
     uint8_t file_type,
     libcerror_error_t **error );

int libpff_allocation_table_read_file_io_handle(
     libcdata_range_list_t *unallocated_block_list,
     libbfio_handle_t *file_io_handle,
     off64_t allocation_table_offset,
     uint8_t file_type,
     libcerror_error_t **error );

#if defined( __cplusplus )
}
#endif

#endif /* !defined( _LIBPFF_ALLOCATION_TABLE_H ) */

