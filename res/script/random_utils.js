function selectFrom(min,max)
{
    var sum = max-min+1;
    return Math.floor(Math.random()*sum+min);
}
//函数2 求指定范围内n个不重复的随机数
function shuffule(n,min,max)
{
    var a = [];
    for(i=0;i<n;i++)
    {
        a[i]=selectFrom(min,max);
        for(z=0;z<i;z++)
        {
            if(a[i]==a[z])
            {
                i--;
                break;
            }
        }

    }
    return a;
}