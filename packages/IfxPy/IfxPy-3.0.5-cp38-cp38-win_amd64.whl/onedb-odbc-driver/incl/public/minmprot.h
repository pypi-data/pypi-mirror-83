/****************************************************************************
 *
 * Licensed Materials - Property of IBM and/or HCL
 *
 * HCL OneDB Client SDK
 * Copyright IBM Corporation 1997, 2008. All rights reserved.
 * (c) Copyright HCL Technologies Ltd. 2017.  All Rights Reserved. 
 *
 *  Title:       minmproto.h
 *  Description: Restricted use memory duration prototypes
 *
 *  Used by datablade developers.
 *
 ***************************************************************************
 */

/*
   The definitions of named memory durations and prototypes are split into
   two separate files to get around build problems in the server. This file
   contains the prototypes. The file incl/public/minamedmem.h includes
   both sub-files as a convenience to the developer.
*/

#ifndef _MINMPROTO_H_
#define _MINMPROTO_H_

#ifndef _MITYPES_H_
#include "mitypes.h"
#endif /*_MITYPES.H_ */

#ifndef _MEMDUR_H_
#include "memdur.h"
#endif  /* not _MEMDUR_H_  */

EXTERNC_BEGIN

/*
 * Named memory allocation calls
 */

/* allocate a named block for the current default duration */
MI_DECL
mi_integer  MI_PROC_EXPORT
mi_named_alloc ARGS((mi_integer 	len,
		     mi_string 		*name,
		     MI_MEMORY_DURATION duration,
		     void 		**memptr));

/* allocate and zero a named block using the specified duration */

MI_DECL
mi_integer  MI_PROC_EXPORT
mi_named_zalloc ARGS((mi_integer 	 len,
		      mi_string 	 *name,
		      MI_MEMORY_DURATION duration,
		      void		 **memptr));

/* retrieve the address of a block by name and duration */

MI_DECL
mi_integer  MI_PROC_EXPORT
mi_named_get ARGS((mi_string 		*name,
		   MI_MEMORY_DURATION 	duration,
		   void			**memptr));

/* free a block specified by name and duration */

MI_DECL
void MI_PROC_EXPORT
mi_named_free ARGS((mi_string 		*name,
		    MI_MEMORY_DURATION 	duration));

/*
 * Routines to manage Mutexes
 */

/* (wait for) and lock a named memory mutex */

MI_DECL
mi_integer  MI_PROC_EXPORT
mi_lock_memory ARGS((mi_string 		*name,
		     MI_MEMORY_DURATION duration));

/* unlock a named memory mutex */

MI_DECL
mi_integer  MI_PROC_EXPORT
mi_unlock_memory ARGS((mi_string 	  *name,
		       MI_MEMORY_DURATION duration));

/* conditionally lock a named memory mutex; return error if already locked */

MI_DECL
mi_integer  MI_PROC_EXPORT
mi_try_lock_memory ARGS((mi_string 	    *name,
		         MI_MEMORY_DURATION duration));
MI_DECL
MI_CONNECTION * MI_PROC_EXPORT
mi_get_session_connection();

MI_DECL
mi_lvarchar * MI_PROC_EXPORT
mi_get_cursor_table(mi_lvarchar *curname);

EXTERNC_END

#endif /* _MINMPROTO_H_ */
