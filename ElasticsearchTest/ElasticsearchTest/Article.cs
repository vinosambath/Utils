using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ElasticsearchTest
{
    class Article
    {
        public string title { get; set; }
        public string artist { get; set; }
        public Article(string Title, string Artist)
        {
            title = Title; artist = Artist;
        }
    }
}
