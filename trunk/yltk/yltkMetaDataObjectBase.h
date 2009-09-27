#ifndef __yltkMetaDataObjectBase_h
#define __yltkMetaDataObjectBase_h

#include "yltkLightObject.h"
#include <typeinfo>
#include <iostream>

namespace yltk{

	/** \class MetaDataObjectBase
	* \brief
	* The MetaDataObjectBase class is designed as the
	* common interface for MetaDataObject's.
	* This class is intended as the value part
	* of the (key,value) pair to be stored in
	* a MetaDataDictionary
	* 
	* \author Hans J. Johnson
	*/
	class MetaDataObjectBase : public LightObject
	{
	public:
		/** Smart pointer typedef support. */
		typedef MetaDataObjectBase        Self;
		typedef LightObject               Superclass;
		typedef SmartPointer<Self>        Pointer;
		typedef SmartPointer<const Self>  ConstPointer;

		/** Run-time type information (and related methods). */
		yltkTypeMacro(MetaDataObjectBase, LightObject);

		/**
		* \author Hans J. Johnson
		* \return A pointer to a const char array containing the unique type name.
		*/
		virtual const char * GetMetaDataObjectTypeName(void) const;
		/**
		* \author Hans J. Johnson
		* \return A constant reference to a std::type_info object
		*/
		virtual const std::type_info & GetMetaDataObjectTypeInfo(void) const;
		/**
		* Defines the default behavior for printing out this element
		* \param os An output stream
		*/
		virtual void Print(std::ostream& os) const;
	protected:
		/** Method for creation through the object factory.   */
		// Should not be able to construct a new MetaDataObjectBase
		//       static  Pointer New(void);
		/**
		* Default destructor
		*/
		virtual ~MetaDataObjectBase();
		MetaDataObjectBase();
	private:
		MetaDataObjectBase(const Self &);//purposely not implemented
		void operator=(const Self&); //purposely not implemented
	};
}

#endif