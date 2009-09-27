#ifndef __yltkEvents_h
#define __yltkEvents_h

/** This file contains the declarations of YLTK Events used to communicate 
*  among components. */

#include "yltkEventObject.h"


//#include "vtkImageData.h"
//#include "vtkPlaneSource.h"
//#include "vtkCamera.h"

namespace yltk{

#define yltkLoadedEventMacro( name, superclass, payloadtype ) \
	class  name : public superclass \
	{ \
	public:  \
		typedef name        Self; \
		typedef superclass  Superclass; \
		typedef payloadtype PayloadType; \
		name() {} \
		virtual ~name() {} \
		virtual const char * GetEventName() const { return #name; } \
		virtual bool CheckEvent(const ::yltk::EventObject* e) const \
			{ return dynamic_cast<const Self*>(e) != NULL ; } \
		virtual ::yltk::EventObject* MakeObject() const \
			{ return new Self; } \
		name(const Self&s) :superclass(s){}; \
		const PayloadType & Get() const \
			{ return m_Payload; }  \
		void Set( const payloadtype & _var ) \
			{ m_Payload = _var; }  \
	private: \
		void operator=(const Self&);  \
		PayloadType  m_Payload; \
};

	namespace EventHelperType 
	{
		//typedef itk::Point< double, 3 >    PointType;
		typedef std::string                StringType;
		//typedef vtkImageData *             VTKImagePointerType;
		//typedef vtkPlaneSource *           VTKPlaneSourcePointerType;
		//typedef vtkCamera *                VTKCameraPointerType;
		typedef unsigned int               UnsignedIntType;
		typedef signed int                 SignedIntType;
		typedef float                      FloatType;
		typedef double                     DoubleType;
		typedef struct {
			unsigned int minimum;
			unsigned int maximum;
		}                                  IntegerBoundsType;
		typedef struct {
			double xmin;
			double xmax;
			double ymin;
			double ymax;
			double zmin;
			double zmax;
		}                                  ImageBoundsType;
		typedef struct {
			unsigned int xmin;
			unsigned int xmax;
			unsigned int ymin;
			unsigned int ymax;
			unsigned int zmin;
			unsigned int zmax;
		}                                  ImageExtentType;
	}

#define yltkLoadedObjectEventMacro( name, superclass, payloadtype ) \
	class  name : public superclass \
	{ \
	public:  \
	typedef name        Self; \
	typedef superclass  Superclass; \
	typedef payloadtype PayloadType; \
	name() {} \
	virtual ~name() {} \
	virtual const char * GetEventName() const { return #name; } \
	virtual bool CheckEvent(const ::yltk::EventObject* e) const \
	{ return dynamic_cast<const Self*>(e) != NULL ; } \
	virtual ::yltk::EventObject* MakeObject() const \
	{ return new Self; } \
	name(const Self&s) :superclass(s){}; \
	PayloadType* Get() const\
	{ return m_Payload.GetPointer(); }  \
	void Set( payloadtype * _var ) \
	{ m_Payload = _var; }  \
	private: \
	void operator=(const Self&);  \
	PayloadType::Pointer  m_Payload; \
};


#define yltkLoadedConstObjectEventMacro( name, superclass, payloadtype ) \
	class  name : public superclass \
	{ \
	public:  \
	typedef name        Self; \
	typedef superclass  Superclass; \
	typedef payloadtype PayloadType; \
	name() {} \
	virtual ~name() {} \
	virtual const char * GetEventName() const { return #name; } \
	virtual bool CheckEvent(const ::yltk::EventObject* e) const \
	{ return dynamic_cast<const Self*>(e) != NULL ; } \
	virtual ::yltk::EventObject* MakeObject() const \
	{ return new Self; } \
	name(const Self&s) :superclass(s){}; \
	const PayloadType* Get() const\
	{ return m_Payload.GetPointer(); }  \
	void Set( const payloadtype * _var ) \
	{ m_Payload = _var; }  \
	private: \
	void operator=(const Self&);  \
	PayloadType::ConstPointer  m_Payload; \
};


#define yltkLoadedTemplatedObjectEventMacro( name, superclass, payloadtype ) \
	class  name : public superclass \
	{ \
	public:  \
	typedef name        Self; \
	typedef superclass  Superclass; \
	typedef payloadtype PayloadType; \
	name() {} \
	virtual ~name() {} \
	virtual const char * GetEventName() const { return #name; } \
	virtual bool CheckEvent(const ::yltk::EventObject* e) const \
	{ return dynamic_cast<const Self*>(e) != NULL ; } \
	virtual ::yltk::EventObject* MakeObject() const \
	{ return new Self; } \
	name(const Self&s) :superclass(s){}; \
	PayloadType * Get() const\
	{ return m_Payload.GetPointer(); }  \
	void Set( payloadtype * _var ) \
	{ m_Payload = _var; }  \
	private: \
	void operator=(const Self&);  \
	typename PayloadType::Pointer  m_Payload; \
};

#define yltkLoadedTemplatedConstObjectEventMacro( name, superclass,\
	payloadtype ) \
	class  name : public superclass \
	{ \
	public:  \
	typedef name        Self; \
	typedef superclass  Superclass; \
	typedef payloadtype PayloadType; \
	name() {} \
	virtual ~name() {} \
	virtual const char * GetEventName() const { return #name; } \
	virtual bool CheckEvent(const ::yltk::EventObject* e) const \
	{ return dynamic_cast<const Self*>(e) != NULL ; } \
	virtual ::yltk::EventObject* MakeObject() const \
	{ return new Self; } \
	name(const Self&s) :superclass(s){}; \
	const PayloadType * Get() const\
	{ return m_Payload.GetPointer(); }  \
	void Set( const payloadtype * _var ) \
	{ m_Payload = _var; }  \
	private: \
	void operator=(const Self&);  \
	typename PayloadType::ConstPointer  m_Payload; \
};

	yltkEventMacro( YLTKErrorEvent,          yltk::UserEvent );
	yltkEventMacro( PulseEvent,               yltk::UserEvent );
	yltkEventMacro( RefreshEvent,             yltk::UserEvent );
	yltkEventMacro( CompletedEvent,           yltk::UserEvent );
	yltkEventMacro( InputOutputErrorEvent,    YLTKErrorEvent );
	yltkEventMacro( InputOutputTimeoutEvent,  YLTKErrorEvent );
	yltkEventMacro( OpenPortErrorEvent,       YLTKErrorEvent );
	yltkEventMacro( ClosePortErrorEvent,      YLTKErrorEvent );
	yltkEventMacro( InvalidRequestErrorEvent, YLTKErrorEvent );
	yltkEventMacro( TransformNotAvailableEvent, InvalidRequestErrorEvent );
	yltkEventMacro( TransformExpiredErrorEvent, TransformNotAvailableEvent );

	//yltkLoadedEventMacro( PointEvent, yltk::UserEvent, EventHelperType::PointType );
	yltkLoadedEventMacro( LandmarkRegistrationErrorEvent, YLTKErrorEvent, 
		EventHelperType::DoubleType );
	yltkLoadedEventMacro( StringEvent, yltk::UserEvent, EventHelperType::StringType );
	yltkLoadedEventMacro( UnsignedIntEvent, yltk::UserEvent, 
		EventHelperType::UnsignedIntType );

	yltkLoadedEventMacro( IntegerBoundsEvent, yltk::UserEvent, 
		EventHelperType::IntegerBoundsType );

	yltkLoadedEventMacro( ImageBoundsEvent, yltk::UserEvent, 
		EventHelperType::ImageBoundsType );

	yltkLoadedEventMacro( ImageExtentEvent, yltk::UserEvent, 
		EventHelperType::ImageExtentType );

	//yltkLoadedEventMacro( VTKImageModifiedEvent, yltk::UserEvent,
	//	EventHelperType::VTKImagePointerType );

	//igstkLoadedEventMacro( VTKPlaneModifiedEvent, IGSTKEvent,
	//                       EventHelperType::VTKPlaneSourcePointerType );

	//yltkLoadedEventMacro( VTKCameraModifiedEvent, yltk::UserEvent,
	//	EventHelperType::VTKCameraPointerType );

	yltkLoadedEventMacro( DoubleTypeEvent, yltk::UserEvent,
		EventHelperType::DoubleType );

	yltkLoadedEventMacro( IGSTKErrorWithStringEvent, YLTKErrorEvent, 
		EventHelperType::StringType );

	yltkEventMacro( AxialSliceBoundsEvent,      IntegerBoundsEvent );
	yltkEventMacro( SagittalSliceBoundsEvent,   IntegerBoundsEvent );
	yltkEventMacro( CoronalSliceBoundsEvent,    IntegerBoundsEvent );

}

#endif