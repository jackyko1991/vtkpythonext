#ifndef __yltkCreateObjectFunction_h
#define __yltkCreateObjectFunction_h

#include "yltkObject.h"

namespace yltk{
	/** \class CreateObjectFunctionBase
	* \brief Define API for object creation callback functions.
	*
	* \ingroup YLTKSystemObjects
	*/
	class CreateObjectFunctionBase: public Object
	{
	public:
		/** Standard typedefs. */
		typedef CreateObjectFunctionBase  Self;
		typedef Object                    Superclass;
		typedef SmartPointer<Self>        Pointer;
		typedef SmartPointer<const Self>  ConstPointer;

		/** Create an object and return a pointer to it as an
		* yltk::LightObject. */
		virtual SmartPointer<LightObject> CreateObject() = 0;

	protected:
		CreateObjectFunctionBase(){}
		~CreateObjectFunctionBase(){}

	private:
		CreateObjectFunctionBase(const Self&);	//purposely not implemented
		void operator=(const Self&); //purposely not implemented
	};

	/** \class CreateObjectFunction
	* \brief CreateObjectFunction is used to create callback functions that
	* create yltk Objects for use with the yltk::ObjectFactory.
	* 
	* \ingroup YLTKSystemObjects
	*/
	template <class T>
	class CreateObjectFunction : public CreateObjectFunctionBase
	{
	public:
		/** Standard class typedefs. */
		typedef CreateObjectFunction  Self;
		typedef SmartPointer<Self>    Pointer;

		/** Methods from yltk:LightObject. */
		yltkFactorylessNewMacro(Self);
		LightObject::Pointer CreateObject() { return T::New().GetPointer(); }

	protected:
		CreateObjectFunction() {}
		~CreateObjectFunction() {}

	private:
		CreateObjectFunction(const Self&); //purposely not implemented
		void operator=(const Self&); //purposely not implemented
	};
}

#endif