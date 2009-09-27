#ifndef __itkMetaDataObject_txx
#define __itkMetaDataObject_txx

#include "yltkMetaDataObject.h"

template<class MetaDataObjectType>
yltk::MetaDataObject<MetaDataObjectType>
::MetaDataObject(void)
{
	//Nothing to do, m_MetaDataObjectValue takes this types default value.
}

template<class MetaDataObjectType>
yltk::MetaDataObject<MetaDataObjectType>
::~MetaDataObject(void)
{
	//std::cout << "                            MetaDataObject Deleteing: " << this << std::endl;
	//Nothing to do here.
}


template<class MetaDataObjectType>
yltk::MetaDataObject<MetaDataObjectType>
::MetaDataObject(const MetaDataObjectType InitializerValue)
:m_MetaDataObjectValue(InitializerValue)
{
	//Nothing to be done here
}

template<class MetaDataObjectType>
yltk::MetaDataObject<MetaDataObjectType>
::MetaDataObject(const MetaDataObject<MetaDataObjectType> &TemplateObject)
:m_MetaDataObjectValue(TemplateObject.m_MetaDataObjectValue)
{
	//Nothing to be done here
}

template<class MetaDataObjectType>
const char *
yltk::MetaDataObject<MetaDataObjectType>
::GetMetaDataObjectTypeName(void) const
{
	return typeid(MetaDataObjectType).name();
}

template<class MetaDataObjectType>
const std::type_info &
yltk::MetaDataObject<MetaDataObjectType>
::GetMetaDataObjectTypeInfo(void) const
{
	return typeid(MetaDataObjectType);
}

template<class MetaDataObjectType>
const MetaDataObjectType &
yltk::MetaDataObject<MetaDataObjectType>
::GetMetaDataObjectValue(void) const
{
	return m_MetaDataObjectValue;
}

template<class MetaDataObjectType>
void
yltk::MetaDataObject<MetaDataObjectType>
::SetMetaDataObjectValue(const MetaDataObjectType & NewValue )
{
	m_MetaDataObjectValue=NewValue;
}

template<class MetaDataObjectType>
void
yltk::MetaDataObject<MetaDataObjectType>
::Print(std::ostream& os) const
{
	//  os << "[UNKNOWN PRINT CHARACTERISTICS]" << std::endl;
	Superclass::Print(os);
}

#endif