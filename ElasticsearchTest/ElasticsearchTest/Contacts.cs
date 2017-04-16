using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ElasticsearchTest
{
    class Contacts
    {
        public string name { get; set; }
        public string country { get; set; }
        public Contacts(string Name, string Country)
        {
            name = Name; country = Country;
        }
    }
}
