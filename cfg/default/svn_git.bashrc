# raccourcis SVN

REP_MT=clifton.ltas.ulg.ac.be/home/metafor/SVN
REP_MTLUB=clifton.ltas.ulg.ac.be/home/metafor/SVN2
REP_GIT=clifton.ltas.ulg.ac.be:/home/metafor/GIT

function oo_meta_co
{
  svn co svn+ssh://$USER@$REP_MT/oo_meta/trunk oo_meta
}

function oo_nda_co
{  
   svn co svn+ssh://$USER@$REP_MT/oo_nda/trunk oo_nda
}

function keygen_co
{
   git clone $USER@$REP_GIT/keygen.git
}

function mtsetup_co
{
   git clone $USER@$REP_GIT/MetaforSetup.git
}

function parasolid_co
{
   git clone $USER@$REP_GIT/parasolid.git
}

function linuxbin_co
{
  svn co svn+ssh://$USER@$REP_MT/linuxbin linuxbin
}

function metafor_co 
{ 
  svn co svn+ssh://$USER@$REP_MT/linuxbin linuxbin
  svn co svn+ssh://$USER@$REP_MT/oo_meta/trunk oo_meta
  svn co svn+ssh://$USER@$REP_MT/oo_nda/trunk oo_nda
  svn co svn+ssh://$USER@$REP_MINE/keygen/trunk keygen 
}




