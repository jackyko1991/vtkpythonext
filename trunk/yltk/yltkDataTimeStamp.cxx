#include "yltkDataTimeStamp.h"
#include "yltkRealTimeClock.h"
#include <typeinfo>
#include <limits>

namespace yltk{
	DataTimeStamp::DataTimeStamp()
	{
		this->m_StartTime       = 0;
		this->m_ExpirationTime  = 0;
	}


	double DataTimeStamp::GetLongestPossibleTime()
	{
		return std::numeric_limits<double>::max();
	}

	double DataTimeStamp::GetZeroValue()
	{
		return 0.0;
	}


	DataTimeStamp DataTimeStamp::ComputeOverlap( DataTimeStamp t1, DataTimeStamp t2 )
	{
		DataTimeStamp t;
		t.m_StartTime      = t1.GetStartTime() > t2.GetStartTime() ?
			t1.GetStartTime() : t2.GetStartTime();
		t.m_ExpirationTime = t1.GetExpirationTime() < t2.GetExpirationTime() ?
			t1.GetExpirationTime() : t2.GetExpirationTime();
		return t;

	}


	DataTimeStamp::~DataTimeStamp()
	{
		this->m_StartTime       = 0;
		this->m_ExpirationTime  = 0;
	}


	const DataTimeStamp & DataTimeStamp::operator=( const DataTimeStamp & inputTimeStamp )
	{
		this->m_StartTime      = inputTimeStamp.m_StartTime;
		this->m_ExpirationTime = inputTimeStamp.m_ExpirationTime;
		return *this;
	}


	void DataTimeStamp::SetStartTimeNowAndExpireAfter(double millisecondsToExpire) 
	{
		this->m_StartTime      = RealTimeClock::GetTimeStamp();
		this->m_ExpirationTime = this->m_StartTime + millisecondsToExpire;
	}


	double DataTimeStamp::GetStartTime() const 
	{
		return this->m_StartTime;
	}


	double DataTimeStamp::GetExpirationTime() const 
	{
		return this->m_ExpirationTime;
	}


	bool DataTimeStamp::IsValidAtTime( double milliseconds ) const
	{
		if( this->m_StartTime > milliseconds )
		{
			return false;
		}

		if( this->m_ExpirationTime < milliseconds )
		{
			return false;
		}

		return true;
	}

	bool DataTimeStamp::IsValidNow() const
	{
		return this->IsValidAtTime( RealTimeClock::GetTimeStamp() );
	}

	void DataTimeStamp::Print(std::ostream& os, yltk::Indent indent) const
	{
		this->PrintHeader(os, indent); 
		this->PrintSelf(os, indent.GetNextIndent());
		this->PrintTrailer(os, indent);
	}


	/**
	* Define a default print header for all objects.
	*/
	void DataTimeStamp::PrintHeader(std::ostream& os, yltk::Indent indent) const
	{
		os << indent << "DataTimeStamp" << " (" << this << ")\n";
	}


	/**
	* Define a default print trailer for all objects.
	*/
	void DataTimeStamp::PrintTrailer(std::ostream& yltkNotUsed(os), 
		yltk::Indent yltkNotUsed(indent)) const
	{

	}


	/**
	* This operator allows all subclasses of LightObject to be printed via <<.
	* It in turn invokes the Print method, which in turn will invoke the
	* PrintSelf method that all objects should define, if they have anything
	* interesting to print out.
	*/
	std::ostream& operator<<(std::ostream& os, const DataTimeStamp& o)
	{
		o.Print(os, 0);
		return os;
	}


	/** Print Self function */
	void DataTimeStamp::PrintSelf( std::ostream& os, yltk::Indent indent ) const
	{
		os << indent << "RTTI typeinfo:    " << typeid( *this ).name() << std::endl;
		os << indent << "Start Time      = " << this->m_StartTime << std::endl;
		os << indent << "Expiration Time = " << this->m_ExpirationTime << std::endl;
	}

}