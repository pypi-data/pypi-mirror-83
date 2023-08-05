/****************************************************************************
 *
 * Licensed Materials - Property of IBM and/or HCL
 *
 * HCL OneDB Client SDK
 * Copyright IBM Corporation 1997, 2008. All rights reserved.
 * (c) Copyright HCL Technologies Ltd. 2017.  All Rights Reserved. 
 *
 *  Title:       miami.h
 *  Description: Virtual Table/Virtual Index Interface
 *
 ************************************************************************
 */

#ifndef MIAMI_INCLUDED
#define MIAMI_INCLUDED

#include "mitypes.h"
#include "milib.h"

typedef struct mi_am_table_desc MI_AM_TABLE_DESC;
typedef struct mi_am_scan_desc  MI_AM_SCAN_DESC;
typedef struct mi_am_rowid_desc MI_AM_ROWID_DESC;
typedef struct mi_am_key_desc   MI_AM_KEY_DESC;
typedef struct mi_am_stats_desc MI_AM_TSTATS_DESC;
typedef struct mi_am_stats_desc MI_AM_ISTATS_DESC;
typedef struct mi_am_qual_desc  MI_AM_QUAL_DESC;
typedef struct mi_capsule	MI_CAPSULE;
typedef struct mi_capsule_91x   MI_CAPSULE_91x;
typedef struct mi_am_check_desc	MI_AM_CHECK_DESC;

typedef enum MI_AM_BOOLOP
{
    MI_BOOLOP_NONE,    /* not a boolean operator. */
    MI_BOOLOP_AND,     /* boolean AND. */
    MI_BOOLOP_OR       /* boolean OR. */
} MI_AM_BOOLOP;

typedef enum MI_AM_VALUE
{
    MI_VALUE_NOT_EVALUATED,   /* qualification is not yet evaluated. */
    MI_VALUE_TRUE,            /* qualification is true. */
    MI_VALUE_FALSE            /* qualification is false. */
} MI_AM_VALUE;

typedef enum MI_LOCK_TYPE
{
    MI_LCK_S,		/* share lock on the table/index */
    MI_LCK_X,		/* exclusive lock on the table/index */
    MI_LCK_IS_S,	/* intention share lock on the table/index,
			   share lock on the row. */
    MI_LCK_IX_X,	/* intention exclusive lock on the table/index,
			   exclusive lock on the row. */
    MI_LCK_SIX_X	/* share intention exclusive lock on the table/index,
			   exclusive lock on the row. */
} MI_LOCK_TYPE;

typedef enum MI_ISOLATION_LEVEL
{
    MI_ISO_NOTRANSACTION,      /* a transaction is not being used. */
    MI_ISO_READUNCOMMITTED,    /* dirty read. */
    MI_ISO_READCOMMITTED,      /* read only committed. */
    MI_ISO_CURSORSTABILITY,    /* guarantee cursor stability. */
    MI_ISO_REPEATABLEREAD,     /* guarantee repeatable reads. */
    MI_ISO_SERIALIZABLE,       /* guarantee serializability. */
    MI_ISO_ERROR = -1          /* error */
} MI_ISOLATION_LEVEL;

typedef enum MI_UPDATE_STAT_MODE
{
    MI_US_NOT_RUNNING = 0,  /* UPDATE STATISTICS is not being run */
    MI_US_LOW,              /* UPDATE STATISTICS is being run in low mode */
    MI_US_MED,              /* UPDATE STATISTICS is being run in medium mode */
    MI_US_HIGH,             /* UPDATE STATISTICS is being run in high mode */
    MI_US_ERROR = -1        /* Error (e.g., bad table descriptor was passed) */
} MI_UPDATE_STAT_MODE;

/* bit fields for options to AM_CHECK */
#define MI_CHECK_EXTENTS_MASK                 0x00000001
#define MI_CHECK_DATA_MASK                    0x00000002
#define MI_CHECK_DATA_BLOBS_MASK              0x00000004
#define MI_DISPLAY_EXTENTS_MASK               0x00000008
#define MI_DISPLAY_DATA_MASK                  0x00000010
#define MI_DISPLAY_DATA_BLOBS_MASK            0x00000020
#define MI_DISPLAY_TPAGES_MASK                0x00000040
#define MI_DISPLAY_CPAGES_MASK                0x00000080
#define MI_DISPLAY_SPACE_MASK                 0x00000100

#define MI_CHECK_IDXKEYS_MASK                 0x00000200
#define MI_CHECK_IDXKEYS_ROWIDS_MASK          0x00000400
#define MI_DISPLAY_IDXKEYS_MASK               0x00000800
#define MI_DISPLAY_IDXKEYS_ROWIDS_MASK        0x00001000
#define MI_DISPLAY_IDXKEYLEAVES_MASK          0x00002000
#define MI_DISPLAY_IDXKEYLEAVES_ROWIDS_MASK   0x00004000
#define MI_DISPLAY_IDXSPACE_MASK              0x00008000
#define MI_CHECK_IDXUSRXTND_MASK              0x00010000
#define MI_CHECK_IDXUSRXARG_MASK              0x00020000

#define MI_CHECK_YES_TO_ALL_MASK              0x00040000
#define MI_CHECK_NO_TO_ALL_MASK               0x00080000

/* flags for MI_TAB_MODE */
#define MI_INPUT_MASK   0x1
#define MI_OUTPUT_MASK  0x2
#define MI_INOUT_MASK   0x4
#define MI_NOLOG_MASK   0x8
#define MI_IO_MODE_MASK 0x7

/* Macros for the result of MI_TAB_MODE */
#define MI_INPUT(n)           \
      ((((n) & MI_INPUT_MASK)  ? MI_TRUE : MI_FALSE ))
#define MI_OUTPUT(n)          \
      ((((n) & MI_OUTPUT_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_INOUT(n)           \
      ((((n) & MI_INOUT_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_NOLOG(n)           \
      ((((n) & MI_NOLOG_MASK) ? MI_TRUE : MI_FALSE ))

/* Macros for AM_CHECK options */
#define MI_CHECK_EXTENTS(op)           \
    ((((op) & MI_CHECK_EXTENTS_MASK) ? MI_TRUE : MI_FALSE))
#define MI_CHECK_DATA(op)              \
    ((((op) & MI_CHECK_DATA_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_CHECK_DATA_BLOBS(op)        \
    ((((op) & MI_CHECK_DATA_BLOBS_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_DISPLAY_EXTENTS(op)         \
    ((((op) & MI_DISPLAY_EXTENTS_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_DISPLAY_DATA(op)            \
    ((((op) & MI_DISPLAY_DATA_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_DISPLAY_DATA_BLOBS(op)      \
    ((((op) & MI_DISPLAY_DATA_BLOBS_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_DISPLAY_TPAGES(op)          \
    ((((op) & MI_DISPLAY_TPAGES_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_DISPLAY_CPAGES(op)          \
    ((((op) & MI_DISPLAY_CPAGES_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_DISPLAY_SPACE(op)           \
    ((((op) & MI_DISPLAY_SPACE_MASK) ? MI_TRUE : MI_FALSE))

#define MI_CHECK_IDXKEYS(op)           \
    ((((op) & MI_CHECK_IDXKEYS_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_CHECK_IDXKEYS_ROWIDS(op)    \
    ((((op) & MI_CHECK_IDXKEYS_ROWIDS_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_DISPLAY_IDXKEYS(op)         \
    ((((op) & MI_DISPLAY_IDXKEYS_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_DISPLAY_IDXKEYS_ROWIDS(op)  \
    ((((op) & MI_DISPLAY_IDXKEYS_ROWIDS_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_DISPLAY_IDXKEYLEAVES(op)    \
    ((((op) & MI_DISPLAY_IDXKEYLEAVES_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_DISPLAY_IDXKEYLEAVES_ROWIDS(op) \
    ((((op) & MI_DISPLAY_IDXKEYLEAVES_ROWIDS_MASK) ? MI_TRUE : MI_FALSE))
#define MI_DISPLAY_IDXSPACE(op)        \
    ((((op) & MI_DISPLAY_IDXSPACE_MASK) ? MI_TRUE : MI_FALSE ))

#define MI_CHECK_YES_TO_ALL(op) \
    ((((op) & MI_CHECK_YES_TO_ALL_MASK) ? MI_TRUE : MI_FALSE ))
#define MI_CHECK_NO_TO_ALL(op) \
    ((((op) & MI_CHECK_NO_TO_ALL_MASK) ? MI_TRUE : MI_FALSE ))

EXTERNC_BEGIN

MI_DECL
mi_string * MI_PROC_EXPORT
mi_tab_name ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_string * MI_PROC_EXPORT
mi_tab_owner ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_id ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_partnum ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_numfrags ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_unsigned_integer MI_PROC_EXPORT
mi_tab_mode ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_tab_istable ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_tab_isindex ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_integer  MI_PROC_VAEXPORT
mi_tab_check_msg ARGS((MI_AM_TABLE_DESC *td,
			mi_integer msg_type,
			char *msg,
			...));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_tab_unique ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_tab_cluster ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_tab_build ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_date * MI_PROC_EXPORT
mi_tab_createdate ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
MI_ROW_DESC * MI_PROC_EXPORT
mi_tab_rowdesc ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
MI_AM_KEY_DESC * MI_PROC_EXPORT
mi_tab_keydesc ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_string * MI_PROC_EXPORT
mi_tab_amparam ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_string * MI_PROC_EXPORT
mi_tab_spacename ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_string * MI_PROC_EXPORT
mi_tab_spaceloc ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_char1 MI_PROC_EXPORT
mi_tab_spacetype ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_nprojs ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_smallint * MI_PROC_EXPORT
mi_tab_projs ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
void * MI_PROC_EXPORT
mi_tab_userdata ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
void MI_PROC_EXPORT
mi_tab_setuserdata ARGS((MI_AM_TABLE_DESC *td,
			 void *ud));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_nparam_exist ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_string * MI_PROC_EXPORT
mi_tab_param_exist ARGS((MI_AM_TABLE_DESC *td, mi_integer p));

MI_DECL
MI_ISOLATION_LEVEL MI_PROC_EXPORT
mi_tab_isolevel ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
MI_UPDATE_STAT_MODE MI_PROC_EXPORT
mi_tab_update_stat_mode ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_niorows ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_setniorows ARGS((MI_AM_TABLE_DESC *td, mi_integer nrows));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_nextrow ARGS((MI_AM_TABLE_DESC *td, MI_ROW **row,
		     mi_integer *rowid, mi_integer *fragid));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_setnextrow ARGS((MI_AM_TABLE_DESC *td, MI_ROW *row,
			mi_integer rowid, mi_integer fragid));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_getrowcol ARGS((MI_AM_TABLE_DESC *td, mi_integer fragid,
                        mi_integer rowid, mi_integer colno, mi_integer *len,
                        char **key, char **row, mi_integer *iserrno ));
MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_execute_background_session ARGS((MI_AM_TABLE_DESC *td, mi_string *udrname));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_indexcolno ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_max_row_size ARGS((MI_AM_TABLE_DESC *td));

MI_DECL
MI_AM_TABLE_DESC * MI_PROC_EXPORT
mi_scan_table ARGS((MI_AM_SCAN_DESC *sd));

MI_DECL
MI_AM_QUAL_DESC * MI_PROC_EXPORT
mi_scan_quals ARGS((MI_AM_SCAN_DESC *sd));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_scan_nprojs ARGS((MI_AM_SCAN_DESC *sd));

MI_DECL
mi_smallint * MI_PROC_EXPORT
mi_scan_projs ARGS((MI_AM_SCAN_DESC *sd));

MI_DECL
void * MI_PROC_EXPORT
mi_scan_userdata ARGS((MI_AM_SCAN_DESC *sd));

MI_DECL
void MI_PROC_EXPORT
mi_scan_setuserdata ARGS((MI_AM_SCAN_DESC *sd,
			  void *ud));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_scan_newquals ARGS((MI_AM_SCAN_DESC *sd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_scan_forupdate ARGS((MI_AM_SCAN_DESC *sd));

MI_DECL
MI_LOCK_TYPE MI_PROC_EXPORT
mi_scan_locktype ARGS((MI_AM_SCAN_DESC *sd));

MI_DECL
MI_ISOLATION_LEVEL MI_PROC_EXPORT
mi_scan_isolevel ARGS((MI_AM_SCAN_DESC *sd));

MI_DECL
void MI_PROC_EXPORT
mi_qual_setvalue ARGS((MI_AM_QUAL_DESC *qd,
		       MI_AM_VALUE v));

MI_DECL
MI_AM_VALUE MI_PROC_EXPORT
mi_qual_value ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_qual_issimple ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_qual_negate ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_qual_commuteargs ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_qual_funcid ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_qual_handlenull ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_smallint MI_PROC_EXPORT
mi_qual_column ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
void MI_PROC_EXPORT
mi_qual_setreopt ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
MI_DATUM MI_PROC_EXPORT
mi_qual_constant ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
MI_DATUM MI_PROC_EXPORT
mi_qual_constant_nohostvar ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_qual_constisnull ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_qual_constisnull_nohostvar ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_qual_const_depends_outer ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_qual_const_depends_hostvar ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_qual_constisknown ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_qual_constispartial ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_qual_needoutput ARGS((MI_AM_QUAL_DESC *qd,
			 mi_integer n));

MI_DECL
void MI_PROC_EXPORT
mi_qual_setoutput ARGS((MI_AM_QUAL_DESC *qd,
			mi_integer n,
			MI_DATUM v,
			mi_boolean f));

MI_DECL
MI_AM_BOOLOP MI_PROC_EXPORT
mi_qual_boolop ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_qual_nquals ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
MI_AM_QUAL_DESC * MI_PROC_EXPORT
mi_qual_qual ARGS((MI_AM_QUAL_DESC *qd,
		   mi_integer n));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_qual_stratnum ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_string * MI_PROC_EXPORT
mi_qual_funcname ARGS((MI_AM_QUAL_DESC *qd));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_key_nkeys ARGS((MI_AM_KEY_DESC *kd));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_key_opclass ARGS((MI_AM_KEY_DESC *kd,
		     mi_integer k));
MI_DECL
mi_string * MI_PROC_EXPORT
mi_key_opclass_name ARGS((MI_AM_KEY_DESC *kd,
                          mi_integer k));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_key_opclass_nstrat ARGS((MI_AM_KEY_DESC *kd,
			    mi_integer k));

MI_DECL
mi_string * MI_PROC_EXPORT
mi_key_opclass_strat ARGS((MI_AM_KEY_DESC *kd,
			   mi_integer k,
			   mi_integer s));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_key_opclass_nsupt ARGS((MI_AM_KEY_DESC *kd,
			   mi_integer k));

MI_DECL
mi_string * MI_PROC_EXPORT
mi_key_opclass_supt ARGS((MI_AM_KEY_DESC *kd,
			  mi_integer k,
			  mi_integer s));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_key_opclass_slvtype ARGS((MI_AM_KEY_DESC *kd,
			     mi_integer k,
			     mi_integer s,
			     mi_boolean *is_slv,
			     MI_TYPEID *slvtypeid));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_key_funcid ARGS((MI_AM_KEY_DESC *kd,
		    mi_integer k));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_key_changed ARGS((MI_AM_KEY_DESC *kd,
                     mi_integer k));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_id_rowid ARGS((MI_AM_ROWID_DESC *rd));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_id_fragid ARGS((MI_AM_ROWID_DESC *rd));

MI_DECL
void MI_PROC_EXPORT
mi_id_setrowid ARGS((MI_AM_ROWID_DESC *rd,
		     mi_integer rowid));

MI_DECL
void MI_PROC_EXPORT
mi_id_setfragid ARGS((MI_AM_ROWID_DESC *rd,
		      mi_integer fragid));

MI_DECL
void MI_PROC_EXPORT
mi_tstats_setnrows ARGS((MI_AM_TSTATS_DESC *sd,
			 mi_integer nrows));

MI_DECL
void MI_PROC_EXPORT
mi_tstats_setnpages ARGS((MI_AM_TSTATS_DESC *sd,
			  mi_integer npages));

MI_DECL
void MI_PROC_EXPORT
mi_istats_setnlevels ARGS((MI_AM_ISTATS_DESC *sd,
			   mi_integer nlevels));

MI_DECL
void MI_PROC_EXPORT
mi_istats_setnleaves ARGS((MI_AM_ISTATS_DESC *sd,
			   mi_integer nleaves));

MI_DECL
void MI_PROC_EXPORT
mi_istats_setnunique ARGS((MI_AM_ISTATS_DESC *sd,
			   mi_integer nunique));

MI_DECL
void MI_PROC_EXPORT
mi_istats_setclust ARGS((MI_AM_ISTATS_DESC *sd,
			 mi_integer clust));

MI_DECL
void MI_PROC_EXPORT
mi_istats_set2lval ARGS((MI_AM_ISTATS_DESC *sd,
			 void *largeval));

MI_DECL
void MI_PROC_EXPORT
mi_istats_set2sval ARGS((MI_AM_ISTATS_DESC *sd,
			 void * smallval));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_eval_am_qual ARGS((MI_ROW *row,
		      MI_AM_QUAL_DESC *qual));

MI_DECL
void MI_PROC_EXPORT
mi_init_am_qual ARGS((MI_AM_QUAL_DESC *qual));

MI_DECL
MI_AM_QUAL_DESC * MI_PROC_EXPORT
mi_qual_findqual ARGS((MI_AM_QUAL_DESC *qd,
                   int colnum, char *funcname, int curr));

MI_DECL
MI_TYPEID * MI_PROC_EXPORT
mi_rowdesc_typeid ARGS((MI_ROW_DESC *rowdesc));

MI_DECL
MI_CAPSULE * MI_PROC_EXPORT
mi_capsule_from_fdesc ARGS((MI_CONNECTION *conn,
			    MI_FUNC_DESC *fdesc));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_capsule_len ARGS((MI_CAPSULE *capsl));

MI_DECL
MI_FUNC_DESC * MI_PROC_EXPORT
mi_capsule_to_fdesc ARGS((MI_CONNECTION *conn,
			  MI_CAPSULE *capsl));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_capsule_free ARGS((MI_CONNECTION *conn,
		      MI_CAPSULE *capsl));

MI_DECL
mi_smallint MI_PROC_EXPORT
mi_set_optcompind ARGS((mi_smallint optcompind));

#ifdef NT_MI_SAPI
MI_DECL
MI_FUNC_DESC *
mi_qual_funcdesc ARGS((MI_AM_QUAL_DESC *qd));
#endif /* This prototype was missing hence it is under NT_MI_SAPI for NT only */

/*
 * Accessors to and on MI_AM_CHECK_DESC for am_check UDR support of oncheck
 */

MI_DECL
MI_AM_CHECK_DESC * MI_PROC_EXPORT
mi_tab_checkdesc ARGS((MI_AM_TABLE_DESC *td));

/* gets what is now being called 'action' in call to am_check udr */
MI_DECL
mi_integer MI_PROC_EXPORT
mi_check_flags ARGS((MI_AM_CHECK_DESC *cd));

/* string (if any) accompanying -u arg. To be parsed/interpreted by
 * am_check as it sees fit.
 */
MI_DECL
mi_string * MI_PROC_EXPORT
mi_check_xtndargs ARGS((MI_AM_CHECK_DESC *cd));

MI_DECL
mi_integer MI_PROC_EXPORT
mi_tab_check_set_ask ARGS((MI_AM_TABLE_DESC *td, mi_integer options));

MI_DECL
mi_boolean MI_PROC_EXPORT
mi_tab_check_is_recheck ARGS((MI_AM_TABLE_DESC *td));

/*This converts a capsule from CAPSULE_VER_ONE_91x to CAPSULE_VER_TWO_92.*/
MI_DECL
MI_CAPSULE *
mi_convert_capsules_v1_v2(MI_CAPSULE_91x *ucap_v1_91x_p);

/*This reverts a capsule from CAPSULE_VER_TWO_92 to CAPSULE_VER_ONE_91x.*/
MI_DECL
MI_CAPSULE_91x *
mi_revert_capsules_v2_v1(MI_CAPSULE *ucap_v2_92_p);

EXTERNC_END

#endif /* MIAMI_INCLUDED */

