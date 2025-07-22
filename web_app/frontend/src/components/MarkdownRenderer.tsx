import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MarkdownRendererProps {
  content: string;
}

const MarkdownRenderer: React.FC<MarkdownRendererProps> = ({ content }) => {
  return (
    <div className="prose prose-invert prose-emerald max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: ({ children }) => (
            <h1 className="text-3xl font-bold text-emerald-400 mb-4 border-b border-emerald-500/30 pb-2">
              {children}
            </h1>
          ),
          h2: ({ children }) => (
            <h2 className="text-2xl font-semibold text-teal-400 mb-3 mt-6">
              {children}
            </h2>
          ),
          h3: ({ children }) => (
            <h3 className="text-xl font-medium text-cyan-400 mb-2 mt-4">
              {children}
            </h3>
          ),
          table: ({ children }) => (
            <div className="overflow-x-auto my-4">
              <table className="min-w-full border border-emerald-500/30 rounded-lg overflow-hidden">
                {children}
              </table>
            </div>
          ),
          th: ({ children }) => (
            <th className="bg-emerald-600/20 text-emerald-300 px-4 py-2 text-left font-semibold border-b border-emerald-500/30">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="px-4 py-2 border-b border-emerald-500/20 text-gray-300">
              {children}
            </td>
          ),
          code: ({ children, className }) => {
            const isInline = !className;
            return isInline ? (
              <code className="bg-emerald-600/20 text-emerald-300 px-1 py-0.5 rounded text-sm">
                {children}
              </code>
            ) : (
              <code className="block bg-slate-800 text-emerald-300 p-3 rounded-lg overflow-x-auto text-sm">
                {children}
              </code>
            );
          },
          blockquote: ({ children }) => (
            <blockquote className="border-l-4 border-emerald-500 pl-4 my-4 italic text-emerald-300 bg-emerald-600/10 py-2 rounded-r">
              {children}
            </blockquote>
          ),
          ul: ({ children }) => (
            <ul className="list-disc list-inside space-y-1 my-4 text-gray-300">
              {children}
            </ul>
          ),
          ol: ({ children }) => (
            <ol className="list-decimal list-inside space-y-1 my-4 text-gray-300">
              {children}
            </ol>
          ),
          li: ({ children }) => (
            <li className="text-gray-300">
              {children}
            </li>
          ),
          strong: ({ children }) => (
            <strong className="font-semibold text-emerald-300">
              {children}
            </strong>
          ),
          em: ({ children }) => (
            <em className="italic text-cyan-300">
              {children}
            </em>
          ),
          hr: () => (
            <hr className="border-emerald-500/30 my-6" />
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownRenderer; 