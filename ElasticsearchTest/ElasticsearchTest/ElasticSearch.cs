using Nest;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ElasticsearchTest
{
    class ElasticSearch
    {
       public ElasticSearch()
        {
            var node = new Uri("http://localhost:9200");
            var settings = new ConnectionSettings(node).DefaultIndex("article");
            var client = new ElasticClient(settings);

            /*if (client.IndexExists("contacts").Exists)
            {
                Console.WriteLine("Index Exists");
                Program.UpsertArticle(client, new Article("The Last Airbender", "Siddharth"), "blog", "article", 1);
                Program.UpsertContact(client, new Contacts("Siddharth Mehta", "India"), "contacts", "contacts", 2);
                Console.WriteLine("Data Indexed Successfully");
            }
            else
            {
                Console.WriteLine("Index Does Not Exist");
            }*/

            var result = client.Search<Article>(s => s
                   .Query(q => q.MatchAll()));

            foreach(var hit in result.Hits)
            {
                Console.WriteLine(hit.Source.artist);
            }

            Console.ReadLine();
        }
    }
}
