#include "yltkMetaDataDictionary.h"
#include "yltkMetaDataObject.h"
#include "yltkObject.h"
#include "yltkExceptionObject.h"
#include <iostream>
#include <complex>
#if 0
#define NATIVE_TYPE_METADATAPRINT(TYPE_NAME) \
	void \
	yltk::MetaDataObject<TYPE_NAME> \
	::Print(std::ostream& os) const \
{ \
	os << this->m_MetaDataObjectValue << std::endl; \
} \
	void \
	yltk::MetaDataObject<const TYPE_NAME> \
	::Print(std::ostream& os) const \
{ \
	os << this->m_MetaDataObjectValue << std::endl; \
}

NATIVE_TYPE_METADATAPRINT(char)
NATIVE_TYPE_METADATAPRINT(char *)
NATIVE_TYPE_METADATAPRINT(char * const)
NATIVE_TYPE_METADATAPRINT(unsigned char)
NATIVE_TYPE_METADATAPRINT(short int)
NATIVE_TYPE_METADATAPRINT(unsigned short int)
NATIVE_TYPE_METADATAPRINT(int)
NATIVE_TYPE_METADATAPRINT(unsigned int)
NATIVE_TYPE_METADATAPRINT(long int)
NATIVE_TYPE_METADATAPRINT(unsigned long int)
NATIVE_TYPE_METADATAPRINT(float)
NATIVE_TYPE_METADATAPRINT(double)
NATIVE_TYPE_METADATAPRINT(std::string)
NATIVE_TYPE_METADATAPRINT(std::complex<float>)
NATIVE_TYPE_METADATAPRINT(std::complex<double>)

#endif

int yltkMetaDataDictionaryTest(int , char * [])
{
	//This is a demo program to show how to put data into a dictionary.
	yltk::MetaDataDictionary MyDictionary;

	//------------------------Testing of native types
	//-------Floats
	yltk::EncapsulateMetaData<float>(MyDictionary,"ASimpleFloatInitalized",static_cast<float>(1.234560F));
	{
		float tempfloat = 0.0;
		const bool IsValidReturn=yltk::ExposeMetaData<float>(MyDictionary,"ASimpleFloatInitalized",tempfloat);
		if(IsValidReturn == true)
		{
			std::cout << tempfloat << std::endl;
		}
		else
		{
			std::cout << "Invalid key, or invalid type specified." << std::endl;
		}
	}

	yltk::EncapsulateMetaData<float>(MyDictionary,"ASimpleFloatChanged",static_cast<float>(-1000.234560F));
	yltk::EncapsulateMetaData<double>(MyDictionary,"ASimpleFloatChanged",static_cast<float>(-0.000000001F));

	//-------Char pointers --  These can be tricky, so be careful!
	yltk::EncapsulateMetaData<const char *>(MyDictionary,"charconst*","Value String");
	const char * value="Value String";
	yltk::EncapsulateMetaData<const char *>(MyDictionary,"charconst*2",value);
	yltk::EncapsulateMetaData<std::string>(MyDictionary,"srtringfromcharconst*",std::string("Value Never Seen"));

	//Other gotchas with the Dictionary
	char * StrandedMemory=new char[2345];
	strcpy(StrandedMemory,"XXXXXXXXXXXXThis is stranded memory that will not be released when the Dictionary is cleaned up");
	//NOTE: Only the pointer is copied, not the data withing the pointer!
	yltk::EncapsulateMetaData<char *>(MyDictionary,"MemoryChangedOutsideOfDictionary",StrandedMemory);
	{
		char * temp = NULL;
		yltk::ExposeMetaData<char *>(MyDictionary,"MemoryChangedOutsideOfDictionary",temp);
		std::cout << "Memory Before Change: "<<temp <<std::endl;
	}
	strcpy(StrandedMemory,"------------This this was changed outside the class, and may cause all types of errors.");
	{
		char * temp = NULL;
		yltk::ExposeMetaData<char *>(MyDictionary,"MemoryChangedOutsideOfDictionary",temp);
		std::cout << "Memory After Change: "<<temp <<std::endl;
	}

	//Print functionality Test
	std::cout << "===========================================================" << std::endl;
	std::cout << "Printing Dictionary" << std::endl;
	MyDictionary.Print(std::cout);


	// Iterator are broken on VS6
#if !(defined(_MSC_VER) && _MSC_VER < 1300)
	std::cout << "Exercise the Iterator access" << std::endl;
	try
	{
		
		yltk::MetaDataDictionary::Iterator itr = MyDictionary.Begin();
		yltk::MetaDataDictionary::Iterator end = MyDictionary.End();

		while( itr != end )
		{
			std::cout << "Key   = " << itr->first << std::endl;
			std::cout << "Value = ";
			itr->second->Print( std::cout );
			std::cout << std::endl;
			++itr;
		}
	}
	catch( yltk::ExceptionObject  & excp )
	{
		std::cerr << "Exception Thrown." << std::endl;
		std::cerr << excp << std::endl;
		return EXIT_FAILURE;
	}
	std::cout << "Exercise the const Iterator access" << std::endl;
	try
	{
		const yltk::MetaDataDictionary & MyConstDictionary = MyDictionary;
		yltk::MetaDataDictionary::ConstIterator itr = MyConstDictionary.Begin();
		yltk::MetaDataDictionary::ConstIterator end = MyConstDictionary.End();

		while( itr != end )
		{
			std::cout << "Key   = " << itr->first << std::endl;
			std::cout << "Value = ";
			itr->second->Print( std::cout );
			std::cout << std::endl;
			++itr;
		}
	}
	catch( yltk::ExceptionObject  & excp )
	{
		std::cerr << "Exception Thrown." << std::endl;
		std::cerr << excp << std::endl;
		return EXIT_FAILURE;
	}
#endif


	//NOTE: Must clean up memory allocated with char * StrandedMemory=new char[2345];
	delete [] StrandedMemory;

	return EXIT_SUCCESS;

}