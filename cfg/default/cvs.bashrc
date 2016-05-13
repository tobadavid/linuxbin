# anciens raccourcis CVS

REP_OE=tintin.ltas.ulg.ac.be:/disc/users/oofelie/Repository
REP_OO=gaston.ltas.ulg.ac.be:/accounts/oofelie/Repository
REP_MT=gaston.ltas.ulg.ac.be:/accounts/metafor/Repository

CVS_RSH=ssh
export CVS_RSH

function cvs_metafor_co 
{ 
  cvs -d :ext:$USER@$REP_OO co -P -d oofelie oofelie-4; 
  cvs -d :ext:$USER@$REP_MT co -P -d oo_meta oo_meta-4; 
  cvs -d :ext:$USER@$REP_MT co -P oo_nda; 
  cvs -d :ext:$USER@$REP_MT co -P z_mesh; 
  cvs -d :ext:$USER@$REP_MT co -P stp2e;
}
