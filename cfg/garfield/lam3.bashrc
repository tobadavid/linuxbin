# raccourcis SVN

REP_LAM3=62.197.103.126/var/svn

function lam3_co
{
    svn co svn+ssh://lam3ltas@$REP_LAM3/LAM3MergedRepository/trunk lam3
}

