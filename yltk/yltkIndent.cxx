#include "yltkIndent.h"


#define YLTK_STD_INDENT 2
#define YLTK_NUMBER_OF_BLANKS 40

namespace yltk{

	static const char blanks[YLTK_NUMBER_OF_BLANKS+1] = "                                        ";

	/**
	* Instance creation.
	*/
	Indent* Indent::New(){ return new Self; }

	/**
	* Determine the next indentation level. Keep indenting by two until the 
	* max of forty.
	*/
	Indent Indent::GetNextIndent(){
		int indent = m_Indent + YLTK_STD_INDENT;
		if ( indent > YLTK_NUMBER_OF_BLANKS ){
			indent = YLTK_NUMBER_OF_BLANKS;
		}
		return indent;
	}

	/**
	* Print out the indentation. Basically output a bunch of spaces.
	*/
	std::ostream& operator<<(std::ostream& os, const Indent& ind)
	{
		os << blanks + (YLTK_NUMBER_OF_BLANKS-ind.m_Indent);
		return os;
	}
}