
function check_login(value)
{
	var x=value;
	if(x=="")
	{
		alert("you must login first");
		return false;
	}
	else{
		return true;
	}
}
function signupcheck(){
	var email=document.forms['myform']['email'].value;
	var email1=document.forms['myform']['email1'].value;
	if(email != email1){
		alert("EMAILS SHOULD BE SAME");
	return false;
	}
	var password=document.forms['myform']['password'].value;
	var password1=document.forms['myform']['pass1'].value;
	if (password != password1)
	{
		alert("PAssword SHOULD BE SAME");
	return false;
	}
	return true;
	
}
function N_word(question){
	var array=question.split(/\b\s+(?!$)/);
	var y="";
	for(i=0;i<array.length;i++){
		if (array[i].includes(',')==true){
			array[i]=array[i].split(',');
			array[i]=array[i].join(' , ');
		}
		if (array[i].includes('+')==true){
			array[i]=array[i].split('+');
			array[i]=array[i].join(' + ');
		}
		if (array[i].includes('/')==true){
			array[i]=array[i].split('/');
			array[i]=array[i].join(' / ');
		}
		if (array[i].includes('-')==true){
			array[i]=array[i].split('-');
			array[i]=array[i].join(' - ');
		}
		var last=array[i].charAt(array[i].length-1);
		if (last=="?" || last=="." || last=="!"){
			array[i]=array[i].split(last);
			array[i]=array[i].join(" "+last+" ");
		}
		y=y+" "+array[i];
	}
	return y;

}
function check_stopwords(word){
	var stopwords = ['?','.',',','"','+','!','i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"];
	var corrected_word=[];
	var word_check=word.split(/\b\s+(?!$)/); //double space haru lai avoid garna
	for(i=0;i<word_check.length;i++){
		if (word_check[i].length>1){
			if (stopwords.includes(word_check[i].toLowerCase())==false){
				(corrected_word.push(word_check[i]));
			}
	}
}
	if(corrected_word.length==0){
		return false;
	}
	else{
		return true;
	}
}
function Question(){
	var question=document.forms['ask']['question'].value;
	x=question.trim();
	if (x.length<7){
		alert("Plase enter valid question");
			return false;

	}
	word=N_word(question);
	word=word.trim();
	check_stop=check_stopwords(word);
	if (check_stop==false){
		alert("Please enter valid question");
		return false;
	}
	fword=word.charAt(0).toUpperCase() + word.slice(1);
	var i=Number(word.length);
	if(word[i-1]!="?" && word[i-1]!="."){
		fword=fword+" "+"?";
	}
	document.forms['ask']['question'].value=fword;
}

// check_search garda ni split garnu parxa , ? haru tesaile validate gareko
function check_search(){
	var question=document.forms['search_form']['search_q'].value;
	word=N_word(question);
	word=word.trim();
	document.forms['search_form']['search_q'].value=word;
}

function check_topic(){
	topic= $( 'input[name="topics"]:checked' ).val();
	if (topic==undefined){
		alert("Please select at least one of the topic");
		return false
	}
	return true;
}