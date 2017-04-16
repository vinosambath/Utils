using Nest;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace ElasticsearchTest
{
    class Program
    {
        static void Main(string[] args)
        {
            ElasticSearch es = new ElasticSearch();
        }

        public static void UpsertArticle(ElasticClient client, Article article, string index, string type, int id)
        {
            var RecordInserted = client.Index(article, p => p
                                    .Index("article")
                                    .Type("articles"));

            if (RecordInserted.ToString() != "")
            {
                Console.WriteLine("Transaction Successful !");
            }
            else
            {
                Console.WriteLine("Transaction Failed");
            }
        }

        public static void UpsertContact(ElasticClient client, Contacts contact, string index, string type, int id)
        {
            var RecordInserted = client.Index(contact, p => p.
                                    Index("contact"));

            if (RecordInserted.ToString() != "")
            {
                Console.WriteLine("Transaction Successful !");
            }
            else
            {
                Console.WriteLine("Transaction Failed");
            }
        }
    }
}
