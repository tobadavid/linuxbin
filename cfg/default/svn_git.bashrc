# raccourcis SVN

REP_MT=blueberry.ltas.ulg.ac.be/home/metafor/SVN
REP_MTLUB=blueberry.ltas.ulg.ac.be/home/metafor/SVN2
REP_GIT=blueberry.ltas.ulg.ac.be:/home/metafor/GIT

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
  git clone git@github.com:ulgltas/linuxbin.git
}

function metafor_co 
{ 
  linuxbin_co
  oo_meta_co
  oo_nda_co
  parasolid_co
}




