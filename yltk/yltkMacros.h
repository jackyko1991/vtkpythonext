#ifndef __yltkMacros_h
#define __yltkMacros_h

#include <cstdlib>

namespace yltk{


#define YLTK_LEAN_AND_MEAN

/** Set built-in type.  Creates member Set"name"() (e.g., SetTimeStep(time)); */
#define  yltkSetMacro(name,type) \
virtual void Set##name (const type & _arg) \
{ \
	if (this->m_##name != _arg) \
	{ \
		this->m_##name = _arg; \
	} \
}

/** Get built-in type.  Creates member Get"name"() (e.g., GetTimeStep(time));
*/
#define yltkGetMacro(name,type) \
virtual const type & Get##name () const \
{ \
	return this->m_##name; \
}

/** New Macro creates a new object of a class that is using SmartPointers. This
* macro differs from the one in ITK in that it DOES NOT uses factories.
* Factories add run-time uncertainty that is undesirable for yltk. */
#define yltkNewMacro(x) \
	static Pointer New(void) \
	{ \
		Pointer smartPtr = ::yltk::ObjectFactory<x>::Create(); \
		if(smartPtr.GetPointer() == NULL) \
		{ \
			smartPtr = new x; \
		} \
		smartPtr->UnRegister(); \
		return smartPtr; \
	} \
	virtual ::yltk::LightObject::Pointer CreateAnother(void) const \
	{ \
		::yltk::LightObject::Pointer smartPtr; \
		smartPtr = x::New().GetPointer(); \
		return smartPtr; \
	}

/** Type Macro defines the GetNameOfClass() method for every class where it is
* invoked. */
#define yltkTypeMacro(thisClass,superclass) \
virtual const char *GetNameOfClass() const {return #thisClass;} 

/** Create a Macro for friend class. This will take care of platform specific
* ways of declaring a class as a friend */
#if defined(__GNUC__) 
	#define  yltkFriendClassMacro(type) friend class type
#else 
	#define  yltkFriendClassMacro(type) friend type
#endif

/** Set character string.  Creates member Set"name"()
* (e.g., SetFilename(char *)). The macro assumes that
* the class member (name) is declared a type std::string. */
#define yltkSetStringMacro(name) \
virtual void Set##name (const char* _arg) \
{ \
	if ( _arg && (_arg == this->m_##name) ) { return;} \
	if (_arg) \
	{ \
		this->m_##name = _arg;\
	} \
	else \
	{ \
		this->m_##name = ""; \
	} \
	this->Modified(); \
} \
virtual void Set##name (const std::string & _arg) \
{ \
	this->Set##name( _arg.c_str() ); \
} \


/** Get character string.  Creates member Get"name"() 
* (e.g., SetFilename(char *)). The macro assumes that
* the class member (name) is declared as a type std::string. */
#define yltkGetStringMacro(name) \
virtual const char* Get##name () const \
{ \
	return this->m_##name.c_str(); \
}

}


/** Macro that defines all the standard elements related to the StateMachine.
*  This macro factorizes code that should always be present when using 
*  the StateMachine. */
#define  yltkStateMachineMacroBase( yltktypename ) \
private: \
	typedef ::yltk::StateMachine< Self > StateMachineType; \
	typedef yltktypename StateMachineType::TMemberFunctionPointer   ActionType; \
	typedef yltktypename StateMachineType::StateType                StateType;  \
	typedef yltktypename StateMachineType::InputType                InputType;  \
	typedef yltktypename StateMachineType::OutputStreamType OutputStreamType; \
	yltkFriendClassMacro( ::yltk::StateMachine< Self > ); \
	StateMachineType     m_StateMachine; \
	typedef ::itk::ReceptorMemberCommand< Self >   ReceptorObserverType; \
	typedef yltktypename ReceptorObserverType::Pointer \
	ReceptorObserverPointer;  \
public:  \
	void ExportStateMachineDescription( OutputStreamType & ostr, \
										bool skipLoops=false ) const \
	{ m_StateMachine.ExportDescription( ostr, skipLoops ); } \
	void ExportStateMachineDescriptionToLTS( OutputStreamType & ostr,\
											bool skipLoops=false ) const \
	{ m_StateMachine.ExportDescriptionToLTS( ostr, skipLoops ); } \
	void ExportStateMachineDescriptionToSCXML( OutputStreamType & ostr,\
											bool skipLoops=false ) const \
	{ m_StateMachine.ExportDescriptionToSCXML( ostr, skipLoops ); }

#define EMPTYPARAMETER

/** This is the StateMachine Macro to be used with non-templated classes */
#define yltkStateMachineMacro()  yltkStateMachineMacroBase( EMPTYPARAMETER )

/** This is the StateMachine Macro to be used with templated classes */
#define yltkStateMachineTemplatedMacro() yltkStateMachineMacroBase( typename )


/** Convenience macro for declaring Inputs to the State Machine */
#define yltkDeclareInputMacro( inputname ) \
	InputType      m_##inputname##Input 


/** Convenience macro for declaring States of the State Machine */
#define yltkDeclareStateMacro( inputname ) \
	StateType      m_##inputname##State 


/** Convenience macro for adding Inputs to the State Machine */
#define yltkAddInputMacro( inputname ) \
	this->m_StateMachine.AddInput( this->m_##inputname##Input,  \
									#inputname"Input" );


/** Convenience macro for adding States to the State Machine */
#define yltkAddStateMacro( statename ) \
	this->m_StateMachine.AddState( this->m_##statename##State,\
									#statename"State" );

/** Convenience macro for adding Transitions to the State Machine */
#define yltkAddTransitionMacro( state1, input, state2, action )   \
	this->m_StateMachine.AddTransition( this->m_##state1##State,   \
	this->m_##input##Input,    \
	this->m_##state2##State,   \
	& Self::action##Processing );


/** Convenience macro for selecting the initial States of the State Machine */
#define yltkSetInitialStateMacro( inputname ) \
	this->m_StateMachine.SelectInitialState( this->m_##inputname##State );


/** Convenience macro for pushing an input in the queue of the State Machine */
#define yltkPushInputMacro( inputname ) \
	this->m_StateMachine.PushInput( this->m_##inputname##Input );


/** Convenience macro for the initial standard traits of a class */
#define yltkStandardClassBasicTraitsMacro( classname, superclassname ) \
	typedef classname                         Self;  \
	typedef superclassname                    Superclass; \
	typedef ::itk::SmartPointer< Self >       Pointer; \
	typedef ::itk::SmartPointer< const Self > ConstPointer; \
	yltkTypeMacro( classname, superclassname);  

/** Convenience macro for traits of an abstract non-templated class */
#define yltkStandardAbstractClassTraitsMacro( classname, superclassname ) \
	yltkStandardClassBasicTraitsMacro( classname, superclassname ) \
	yltkStateMachineMacro(); 

/** Convenience macro for traits of a non-templated class */
#define yltkStandardClassTraitsMacro( classname, superclassname ) \
	yltkStandardAbstractClassTraitsMacro( classname, superclassname ) \
	yltkNewMacro( Self );  

/** Convenience macro for the traits of an abstract templated class */
#define yltkStandardTemplatedAbstractClassTraitsMacro( classname, \
	superclassname ) \
	yltkStandardClassBasicTraitsMacro( classname, superclassname ) \
	yltkStateMachineTemplatedMacro(); 

/** Convenience macro for the traits of a templated class */
#define yltkStandardTemplatedClassTraitsMacro( classname, superclassname ) \
	yltkStandardTemplatedAbstractClassTraitsMacro( classname, superclassname ) \
	yltkNewMacro( Self );


/** This macro is used to print debug (or other information). They are
* also used to catch errors, etc. Example usage looks like:
* yltkDebugMacro(<< "this is debug info" << this->SomeVariable); */
#if defined(YLTK_LEAN_AND_MEAN) || defined(__BORLANDC__) || defined(NDEBUG)
#define yltkDebugMacro(x)
#else
#define yltkDebugMacro(x) \
  { if (this->GetDebug() && ::yltk::Object::GetGlobalWarningDisplay())   \
	{ ::yltk::OStringStream yltkmsg; \
	yltkmsg << "Debug: In " __FILE__ ", line " << __LINE__ << "\n" \
	<< this->GetNameOfClass() << " (" << this << "): " x  \
	<< "\n\n"; \
	::yltk::OutputWindowDisplayDebugText(itkmsg.str().c_str());} \
}
#endif

/** Define two object creation methods.  The first method, New(),
* creates an object from a class but does not defer to a factory.
* The second method, CreateAnother(), creates an object from an
* instance, again without deferring to a factory.  This second method
* allows you to create an instance of an object that is exactly the
* same type as the referring object.  This is useful in cases where
* an object has been cast back to a base class.
*
* These creation methods first try asking the object factory to create
* an instance, and then default to the standard "new" operator if the
* factory fails.
*
* These routines assigns the raw pointer to a smart pointer and then call
* UnRegister() on the rawPtr to compensate for LightObject's constructor
* initializing an object's reference count to 1 (needed for proper
* initialization of process objects and data objects cycles). */
#define yltkFactorylessNewMacro(x) \
	static Pointer New(void) \
	{ \
		Pointer smartPtr; \
		x *rawPtr = new x; \
		smartPtr = rawPtr; \
		rawPtr->UnRegister(); \
		return smartPtr; \
	} \
	virtual ::yltk::LightObject::Pointer CreateAnother(void) const \
	{ \
		::itk::LightObject::Pointer smartPtr;         \
		smartPtr = x::New().GetPointer(); \
		return smartPtr; \
	}


#ifdef YLTK_LEAN_AND_MEAN
#define yltkGenericOutputMacro(x)
#else
#define yltkGenericOutputMacro(x) \
{ if (::yltk::Object::GetGlobalWarningDisplay()) \
	{ ::yltk::OStringStream yltkmsg; \
	yltkmsg << "WARNING: In " __FILE__ ", line " << __LINE__ << "\n" \
	x << "\n\n"; \
	::yltk::OutputWindowDisplayGenericOutputText(yltkmsg.str().c_str());} \
}
#endif

/** This macro is used to print warning information (i.e., unusual circumstance
* but not necessarily fatal.) Example usage looks like:
* itkWarningMacro(<< "this is warning info" << this->SomeVariable); */
#ifdef YLTK_LEAN_AND_MEAN
#define yltkWarningMacro(x)
#else
#define yltkWarningMacro(x) \
{ if (::yltk::Object::GetGlobalWarningDisplay()) \
	{ ::yltk::OStringStream yltkmsg; \
	yltkmsg << "WARNING: In " __FILE__ ", line " << __LINE__ << "\n" \
	<< this->GetNameOfClass() << " (" << this << "): " x  \
	<< "\n\n"; \
	::yltk::OutputWindowDisplayWarningText(itkmsg.str().c_str());} \
}
#endif

/** A convenience macro marks variables as not being used by a method,
* avoiding compile-time warnings. */
#define yltkNotUsed(x)

#endif