#include "yltkMetaDataObjectBase.h"
#include "yltkObjectFactory.h"
#include "yltkCommand.h"
#include "yltkFastMutexLock.h"

void yltk::MetaDataObjectBase::Print(std::ostream& os) const
{
	os << "[UNKNOWN_PRINT_CHARACTERISTICS]" << std::endl;
}


const char * yltk::MetaDataObjectBase::GetMetaDataObjectTypeName(void) const
{
	return typeid(yltk::MetaDataObjectBase).name();
}

const std::type_info &yltk::MetaDataObjectBase::GetMetaDataObjectTypeInfo(void) const
{
	return typeid(yltk::MetaDataObjectBase);
}

yltk::MetaDataObjectBase::MetaDataObjectBase()
{
	//Nothing to do here
}

yltk::MetaDataObjectBase::~MetaDataObjectBase()
{
	
}

#if __THIS_IS_UNNECESSARY_CODE__
yltk::MetaDataObjectBase::Pointer yltk::MetaDataObjectBase::New(void)
{
	Pointer smartPtr;
	yltk::MetaDataObjectBase *rawPtr = ::yltk::ObjectFactory<yltk::MetaDataObjectBase>::Create();
	if(rawPtr == NULL)
	{
		rawPtr = new yltk::MetaDataObjectBase;
	}
	smartPtr = rawPtr;
	rawPtr->UnRegister();
	return smartPtr;
}
#endif