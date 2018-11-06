/**
 * Created by tarena on 18-11-6.
 */
function fun() {
    if(window.XMLHttpRequest){
        return new XMLHttpRequest();
    }else {
        return new ActiveXObject("Microsoft.XMLHTTP");
    }
}

