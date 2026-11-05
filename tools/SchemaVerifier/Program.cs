using System.Reflection.Metadata;
using System.Reflection.PortableExecutable;
using System.Text.Json;

using var stream = File.OpenRead(args[0]);
using var pe = new PEReader(stream);
var metadata = pe.GetMetadataReader();
var rows = new List<object>();
foreach (var handle in metadata.TypeDefinitions)
{
    var type = metadata.GetTypeDefinition(handle);
    foreach (var attributeHandle in type.GetCustomAttributes())
    {
        var attribute = metadata.GetCustomAttribute(attributeHandle);
        if (attribute.Constructor.Kind != HandleKind.MemberReference) continue;
        var constructor = metadata.GetMemberReference((MemberReferenceHandle)attribute.Constructor);
        if (constructor.Parent.Kind != HandleKind.TypeReference) continue;
        var attributeType = metadata.GetTypeReference((TypeReferenceHandle)constructor.Parent);
        if (metadata.GetString(attributeType.Name) != "SheetAttribute") continue;
        var blob = metadata.GetBlobReader(attribute.Value);
        if (blob.ReadUInt16() != 1) throw new InvalidDataException();
        var name = blob.ReadSerializedString();
        var hash = blob.ReadUInt32();
        rows.Add(new { type = metadata.GetString(type.Name), sheet = name, hash });
    }
}
Console.WriteLine(JsonSerializer.Serialize(rows));
